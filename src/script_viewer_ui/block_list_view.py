from PyQt5.QtCore import QModelIndex, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPainter, QPaintEvent, QWheelEvent
from PyQt5.QtWidgets import QAbstractItemView, QListView

from script_viewer_ui import theme
from script_viewer_ui.block_delegate import BlockDelegate
from script_viewer_ui.block_list_model import BlockListModel
from script_viewer_ui.cue_lane_footer import CueLaneFooter
from script_viewer_ui.cue_lane_header import CueLaneHeader
from script_viewer_ui.cue_lane_painter import CueLanePainter
from script_viewer_ui.cue_lane_segments import LISP_LANE, X32_LANE, LIGHT_CUE_LANE, LANES
from script_viewer_ui.row_layout import RowLayout
from script_viewer_ui.viewer_settings import POSITION_BOTTOM, POSITION_TOP, ViewerSettings
from script_viewer_ui.cue_lane import CueLane

WHEEL_NOTCH = 120
PAGE_STEP = 10
RELAYOUT_DELAY_MS = 100


class BlockListView(QListView):
    """The document of block cards, navigated block by block instead of pixel by pixel."""

    current_row_changed = pyqtSignal(int)
    return_pressed = pyqtSignal()

    def __init__(self, model: BlockListModel, settings: ViewerSettings, parent=None):
        super().__init__(parent)
        self._wheel_delta = 0
        self._visible_lanes = self._get_visible_lanes(settings)
        self._settings = settings
        self._delegate = BlockDelegate(model.cue_lanes, self)
        self._cue_lane_painter = CueLanePainter(model.cue_lanes)
        self.setModel(model)
        self.setItemDelegate(self._delegate)

        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setUniformItemSizes(False)
        self.setStyleSheet(_STYLE_SHEET)

        self._header = CueLaneHeader(self)
        self._footer = CueLaneFooter(model.cue_lanes, self)
        self._footer.set_current_row(model.current_row)
        self._update_lane_margins()
        
        self._relayout_timer = QTimer(self, singleShot=True, interval=RELAYOUT_DELAY_MS)
        self._relayout_timer.timeout.connect(self._relayout)

        self.clicked.connect(self._on_clicked)
        self._delegate.set_viewport_width(self.viewport().width())
        self.apply_settings(settings)

    @property
    def _block_model(self) -> BlockListModel:
        return self.model()

    def set_current_row(self, row: int) -> None:
        row = max(0, min(row, self._block_model.rowCount() - 1))
        if row < 0:
            return
        self._block_model.set_current_row(row)
        self._scroll_to_current_row()
        self.viewport().update()
        self._footer.set_current_row(row)
        self.current_row_changed.emit(row)

    def apply_settings(self, settings: ViewerSettings) -> None:
        self._settings = settings
        self._visible_lanes = self._get_visible_lanes(settings)
        self._delegate.set_visible_lanes(self._visible_lanes)
        self._header.set_visible_lanes(self._visible_lanes)
        self._footer.set_visible_lanes(self._visible_lanes)
        self._update_lane_margins()
        self._delegate.set_lane_width(settings.lane_width)
        self._header.set_lane_width(settings.lane_width)
        self._footer.set_lane_width(settings.lane_width)
        self.scheduleDelayedItemsLayout()
        self._scroll_to_current_row()
        self.viewport().update()

    def move_by(self, steps: int) -> None:
        self.set_current_row(self._block_model.current_row + steps)

    def wheelEvent(self, event: QWheelEvent) -> None:
        self._wheel_delta += event.angleDelta().y()
        steps = int(self._wheel_delta / WHEEL_NOTCH)
        if steps:
            self._wheel_delta -= steps * WHEEL_NOTCH
            self.move_by(-steps)
        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key in (Qt.Key_Down, Qt.Key_Right, Qt.Key_Space):
            self.move_by(1)
        elif key in (Qt.Key_Up, Qt.Key_Left, Qt.Key_Backspace):
            self.move_by(-1)
        elif key == Qt.Key_PageDown:
            self.move_by(PAGE_STEP)
        elif key == Qt.Key_PageUp:
            self.move_by(-PAGE_STEP)
        elif key == Qt.Key_Home:
            self.set_current_row(0)
        elif key == Qt.Key_End:
            self.set_current_row(self._block_model.rowCount() - 1)
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if not event.isAutoRepeat():
                self.return_pressed.emit()
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._place_lane_bars()
        self._relayout_timer.start()
        self._scroll_to_current_row()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)
        layout = RowLayout(0, self.viewport().width(), self._visible_lanes, self._settings.lane_width)
        self._cue_lane_painter.paint(painter, 
                                     layout, 
                                     self.viewport().height(),
                                     self._block_model.current_row, 
                                     self._row_span)

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        # Scrolling moves the already painted pixels, which would drag the sticky cue names along.
        super().scrollContentsBy(dx, dy)
        self.viewport().update()

    def _update_lane_margins(self) -> None:
        has_lanes = bool(self._visible_lanes)
        self._header.setVisible(has_lanes)
        self._footer.setVisible(has_lanes)
        if has_lanes:
            self.setViewportMargins(0, self._header.height(), 0, self._footer.height())
        else:
            self.setViewportMargins(0, 0, 0, 0)
        self._place_lane_bars()

    def _place_lane_bars(self) -> None:
        viewport = self.viewport().geometry()
        self._header.setGeometry(viewport.x(), viewport.y() - self._header.height(), viewport.width(), self._header.height())
        self._footer.setGeometry(viewport.x(), viewport.y() + viewport.height(), viewport.width(), self._footer.height())

    def _row_span(self, row: int) -> tuple[int, int]:
        rect = self.visualRect(self._block_model.index(row))
        return rect.top(), rect.top() + rect.height()

    def _on_clicked(self, index: QModelIndex) -> None:
        self.set_current_row(index.row())

    def _relayout(self) -> None:
        if self._delegate.set_viewport_width(self.viewport().width()):
            self.scheduleDelayedItemsLayout()
        self._scroll_to_current_row()

    def _scroll_to_current_row(self) -> None:
        if self._block_model.rowCount() == 0:
            return
        row = self.visualRect(self._block_model.index(self._block_model.current_row))
        free_space = max(self.viewport().height() - row.height(), 0)
        position = self._settings.current_block_position - POSITION_TOP
        target_top = free_space * position // (POSITION_BOTTOM - POSITION_TOP)
        scroll_bar = self.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.value() + row.top() - target_top)

    def _get_visible_lanes(self, settings: ViewerSettings) -> tuple[CueLane, ...]:
        shown = {LISP_LANE: settings.show_lisp_lane, X32_LANE: settings.show_x32_lane,
                 LIGHT_CUE_LANE: settings.show_light_cue_lane}
        return tuple(lane for lane in LANES if shown[lane])


_STYLE_SHEET = f"""
QListView {{
    background-color: {theme.PAGE.name()};
    border: none;
    outline: none;
}}
QScrollBar:vertical {{
    background: {theme.PAGE.name()};
    width: 12px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {theme.SCROLLBAR_HANDLE.name()};
    border-radius: 4px;
    min-height: 40px;
    margin: 2px;
}}
QScrollBar::handle:vertical:hover {{
    background: {theme.SCROLLBAR_HANDLE_HOVER.name()};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
"""
