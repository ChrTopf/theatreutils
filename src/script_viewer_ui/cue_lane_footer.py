from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QFontMetrics, QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget

from script_viewer_ui import theme
from script_viewer_ui.cue_lanes import LANES, CueLane, CueLaneSegments
from script_viewer_ui.cue_style import CueStyle
from script_viewer_ui.row_layout import RowLayout

# Shown in place of a cue name if no further cue follows in the lane.
NO_NEXT_CUE = "—"


class CueLaneFooter(QWidget):
    """The strip below the document showing the next cue of every visible lane, each one under its lane."""

    def __init__(self, cue_lanes: CueLaneSegments, parent=None):
        super().__init__(parent)
        self._cue_lanes = cue_lanes
        self._font = CueStyle.cue_name_font()
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

            if segment is None:
                painter.drawText(text, Qt.AlignCenter, name)
                continue

            counter = str(segment.first_row - self._current_row)
            counter_width = metrics.horizontalAdvance(counter)
            painter.setPen(theme.MUTED_LABEL)
            painter.drawText(text, Qt.AlignRight | Qt.AlignVCenter, counter)

            name_rect = text.adjusted(0, 0, -(counter_width + theme.LANE_LABEL_PADDING), 0)
            painter.setPen(color)
            painter.drawText(name_rect, Qt.AlignLeft | Qt.AlignVCenter, metrics.elidedText(name, Qt.ElideRight, name_rect.width()))
