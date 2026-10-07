from PyQt5.QtCore import QModelIndex, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPainter, QPaintEvent, QWheelEvent
from PyQt5.QtWidgets import QAbstractItemView, QListView

from script_viewer_ui import theme
from script_viewer_ui.block_delegate import BlockDelegate
from script_viewer_ui.block_list_model import BlockListModel
from script_viewer_ui.cue_lane_header import CueLaneHeader
from script_viewer_ui.cue_lane_painter import CueLanePainter
from script_viewer_ui.row_layout import RowLayout

# One notch of a regular mouse wheel, see QWheelEvent.angleDelta().
WHEEL_NOTCH = 120
PAGE_STEP = 10
RELAYOUT_DELAY_MS = 100


class BlockListView(QListView):
    """The document of block cards, navigated block by block instead of pixel by pixel.

    The scroll wheel and the arrow keys move the current block, which is always
    kept in the vertical center of the view. Clicking a block makes it current.

    The cue lanes right of the cards span many rows, so they are painted over
    the whole viewport after the rows. Their names sit in a header above the
    viewport, so they never cover the cue bars.
    """

    current_row_changed = pyqtSignal(int)

    def __init__(self, model: BlockListModel, parent=None):
        super().__init__(parent)
        self._wheel_delta = 0
        self._delegate = BlockDelegate(self)
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
        self.setViewportMargins(0, self._header.height(), 0, 0)

        # Wrapped text changes its height whenever the width changes, so all cards have
        # to be re-measured - but only once the resizing has settled down.
        self._relayout_timer = QTimer(self, singleShot=True, interval=RELAYOUT_DELAY_MS)
        self._relayout_timer.timeout.connect(self._relayout)

        self.clicked.connect(self._on_clicked)
        self._delegate.set_viewport_width(self.viewport().width())

    @property
    def _block_model(self) -> BlockListModel:
        return self.model()

    def set_current_row(self, row: int) -> None:
        row = max(0, min(row, self._block_model.rowCount() - 1))
        if row < 0:
            return
        self._block_model.set_current_row(row)
        self._center_current_row()
        # The highlighted cues span far more rows than the two the model reports as changed.
        self.viewport().update()
        self.current_row_changed.emit(row)

    def move_by(self, steps: int) -> None:
        self.set_current_row(self._block_model.current_row + steps)

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Touchpads report many small deltas, so they are accumulated to full notches.
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
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        viewport = self.viewport().geometry()
        self._header.setGeometry(viewport.x(), viewport.y() - self._header.height(), viewport.width(), self._header.height())
        self._relayout_timer.start()
        self._center_current_row()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing)
        self._cue_lane_painter.paint(painter, RowLayout(0, self.viewport().width()), self.viewport().height(),
                                     self._block_model.current_row, self._row_span)

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        # Scrolling moves the already painted pixels, which would drag the sticky cue names along.
        super().scrollContentsBy(dx, dy)
        self.viewport().update()

    def _row_span(self, row: int) -> tuple[int, int]:
        rect = self.visualRect(self._block_model.index(row))
        return rect.top(), rect.top() + rect.height()

    def _on_clicked(self, index: QModelIndex) -> None:
        self.set_current_row(index.row())

    def _relayout(self) -> None:
        if self._delegate.set_viewport_width(self.viewport().width()):
            self.scheduleDelayedItemsLayout()
        self._center_current_row()

    def _center_current_row(self) -> None:
        if self._block_model.rowCount() > 0:
            self.scrollTo(self._block_model.index(self._block_model.current_row), QAbstractItemView.PositionAtCenter)


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
