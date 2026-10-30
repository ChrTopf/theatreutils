from typing import Callable

from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QFontMetrics, QPainter

from script_viewer_ui import theme
from script_viewer_ui.cue_lanes import CueLaneSegments, CueSegment
from script_viewer_ui.cue_style import CueStyle
from script_viewer_ui.row_layout import RowLayout

class CueLanePainter:
    """Paints the visible cue lanes right of the block cards: one colored bar per cue with its name beside it.

    A bar runs down from the block triggering the cue to the block before the
    next cue of the lane. The name starts at the top of the bar, but sticks to
    the upper edge of the view while the top of the bar is scrolled out, until
    the end of the bar pushes it out as well. Below the name, a smaller line
    tells the location of the triggering block. The cue active at the current
    block is drawn in full color, all others are dimmed.
    """

    def __init__(self, cue_lanes: CueLaneSegments):
        self._cue_lanes = cue_lanes

    def paint(self, painter: QPainter, layout: RowLayout, viewport_height: int,
              current_row: int, row_span: Callable[[int], tuple[int, int]]) -> None:
        for lane in layout.lanes:
            lane_rect = layout.lane_rect(lane, 0, viewport_height)
            for segment in self._cue_lanes.of_lane(lane):
                top = row_span(segment.first_row)[0]
                # Rows end with the spacing below their card, which the bar leaves out like the card does.
                bottom = row_span(segment.last_row)[1] - theme.BLOCK_SPACING
                if bottom < 0 or top > viewport_height:
                    continue
                color = segment.color if segment.contains(current_row) else segment.color.darker(theme.DIMMED_CUE_FACTOR)
                self._paint_bar(painter, lane_rect, top, bottom, color)
                self._paint_label(painter, lane_rect, top, bottom, segment, color)

    @staticmethod
    def _paint_bar(painter: QPainter, lane_rect: QRect, top: int, bottom: int, color: QColor) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        radius = theme.CUE_BAR_WIDTH / 2
        painter.drawRoundedRect(QRectF(lane_rect.x(), top, theme.CUE_BAR_WIDTH, bottom - top), radius, radius)

    @staticmethod
    def _paint_label(painter: QPainter, lane_rect: QRect, top: int, bottom: int,
                     segment: CueSegment, color: QColor) -> None:
        label_top = max(top + theme.BLOCK_PADDING, theme.CUE_NAME_STICKY_MARGIN)
        label_top = min(label_top, bottom - CueStyle.cue_label_height(len(segment.names)))

        left = lane_rect.x() + theme.CUE_BAR_WIDTH + theme.LANE_LABEL_PADDING
        width = lane_rect.right() - left - theme.LANE_LABEL_PADDING
        painter.setPen(color)

        font = CueStyle.cue_name_font()
        painter.setFont(font)
        metrics = QFontMetrics(font)
        line = QRect(left, label_top, width, metrics.lineSpacing())
        for name in segment.names:
            painter.drawText(line, Qt.AlignLeft | Qt.AlignVCenter, metrics.elidedText(name, Qt.ElideMiddle, line.width()))
            line.translate(0, metrics.lineSpacing())

        font = CueStyle.cue_location_font()
        painter.setFont(font)
        metrics = QFontMetrics(font)
        line.setHeight(metrics.lineSpacing())
        painter.drawText(line, Qt.AlignLeft | Qt.AlignVCenter,
                         metrics.elidedText(segment.location, Qt.ElideRight, line.width()))
