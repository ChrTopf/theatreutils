from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QFontMetrics, QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget

from script_viewer_ui import theme
from script_viewer_ui.cue_lane_painter import cue_name_font
from script_viewer_ui.cue_lanes import LANES, CueLane, CueLaneSegments
from script_viewer_ui.row_layout import RowLayout

# Shown in place of a cue name if no further cue follows in the lane.
NO_NEXT_CUE = "—"


class CueLaneFooter(QWidget):
    """The strip below the document showing the next cue of every visible lane, each one centered under its lane.

    It lies outside of the scrolled area, so the next cues are always visible.
    Its width has to match the viewport of the document, so the RowLayout puts
    the names under the same lanes as the rows above. The next cue is drawn in
    the color its bar will have, if a block triggers several cues of a lane at
    once, the first one is shown.
    """

    def __init__(self, cue_lanes: CueLaneSegments, parent=None):
        super().__init__(parent)
        self._cue_lanes = cue_lanes
        self._font = cue_name_font()
        self._label_height = QFontMetrics(self._font).height() + theme.LANE_LABEL_PADDING
        self.setFixedHeight(self._label_height + 2 * theme.LANE_LABEL_MARGIN)
        self._visible_lanes = LANES
        self._current_row = 0

    def set_visible_lanes(self, lanes: tuple[CueLane, ...]) -> None:
        self._visible_lanes = lanes
        self.update()

    def set_current_row(self, row: int) -> None:
        self._current_row = row
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), theme.PAGE)
        painter.setFont(self._font)
        metrics = QFontMetrics(self._font)
        layout = RowLayout(0, self.width(), self._visible_lanes)
        radius = theme.BLOCK_CORNER_RADIUS

        for lane in layout.lanes:
            label = layout.lane_rect(lane, theme.LANE_LABEL_MARGIN, self._label_height)
            segment = self._cue_lanes.next_segment(lane, self._current_row)
            name = segment.names[0] if segment else NO_NEXT_CUE
            color = segment.color if segment else theme.MUTED_LABEL

            painter.setPen(color)
            painter.setBrush(theme.LANE_LABEL_BACKGROUND)
            painter.drawRoundedRect(QRectF(label).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
            text = QRect(label).adjusted(theme.LANE_LABEL_PADDING, 0, -theme.LANE_LABEL_PADDING, 0)
            painter.drawText(text, Qt.AlignCenter, metrics.elidedText(name, Qt.ElideRight, text.width()))
