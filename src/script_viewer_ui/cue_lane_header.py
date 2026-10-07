from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget

from script_viewer_ui import theme
from script_viewer_ui.cue_lanes import LANES
from script_viewer_ui.row_layout import RowLayout


class CueLaneHeader(QWidget):
    """The strip above the document holding the names of the cue lanes, each one centered over its lane.

    It lies outside of the scrolled area, so the names never cover the cue bars.
    Its width has to match the viewport of the document, so the RowLayout puts
    the names over the same lanes as the rows below.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = QFont()
        self._font.setPointSize(theme.LANE_LABEL_POINT_SIZE)
        self._font.setBold(True)
        self._label_height = QFontMetrics(self._font).height() + theme.LANE_LABEL_PADDING
        self.setFixedHeight(self._label_height + 2 * theme.LANE_LABEL_MARGIN)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), theme.PAGE)
        painter.setFont(self._font)
        metrics = QFontMetrics(self._font)
        layout = RowLayout(0, self.width())
        radius = self._label_height / 2

        for lane_index, lane in enumerate(LANES):
            lane_rect = layout.lane_rect(lane_index, theme.LANE_LABEL_MARGIN, self._label_height)
            width = min(metrics.horizontalAdvance(lane.name) + 2 * theme.LANE_LABEL_PADDING, lane_rect.width())
            label = QRect(lane_rect.center().x() - width // 2, lane_rect.y(), width, self._label_height)

            painter.setPen(lane.color)
            painter.setBrush(theme.LANE_LABEL_BACKGROUND)
            painter.drawRoundedRect(QRectF(label).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
            painter.drawText(label, Qt.AlignCenter, metrics.elidedText(lane.name, Qt.ElideRight, width))
