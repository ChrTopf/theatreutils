from PyQt5.QtCore import QModelIndex, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QWheelEvent
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableView

from script_viewer_ui import theme
from script_viewer_ui.block_table_model import BlockTableModel, MIC_COLUMN, TEXT_COLUMN
from script_viewer_ui.mic_cue_delegate import MicCueDelegate

# One notch of a regular mouse wheel, see QWheelEvent.angleDelta().
WHEEL_NOTCH = 120
PAGE_STEP = 10
ROW_RESIZE_DELAY_MS = 100


class BlockTableView(QTableView):
    """The block table that is navigated block by block instead of pixel by pixel.

    The scroll wheel and the arrow keys move the current block, which is always
    kept in the vertical center of the view. Clicking a block makes it current.
    """

    current_row_changed = pyqtSignal(int)

    def __init__(self, model: BlockTableModel, parent=None):
        super().__init__(parent)
        self._wheel_delta = 0
        self.setModel(model)
        self.setItemDelegateForColumn(MIC_COLUMN, MicCueDelegate(self))

        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setWordWrap(True)
        self.setShowGrid(True)
        self.setStyleSheet(
            f"QTableView {{ background-color: {theme.BACKGROUND.name()}; gridline-color: {theme.GRID.name()}; border: none; }}"
            f"QHeaderView::section {{ background-color: {theme.GRID.name()}; color: {theme.TEXT.name()}; "
            f"padding: 4px; border: none; font-weight: bold; }}"
        )
        self.verticalHeader().hide()

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        for column in range(model.columnCount()):
            if column != TEXT_COLUMN:
                self.resizeColumnToContents(column)
                header.resizeSection(column, max(header.sectionSize(column), 140))

        # Wrapped text changes its height whenever a column width changes, so the
        # row heights are recalculated once the resizing has settled down.
        self._row_resize_timer = QTimer(self, singleShot=True, interval=ROW_RESIZE_DELAY_MS)
        self._row_resize_timer.timeout.connect(self._resize_rows)
        header.sectionResized.connect(lambda *_: self._row_resize_timer.start())

        self.clicked.connect(self._on_clicked)
        self._resize_rows()

    @property
    def _block_model(self) -> BlockTableModel:
        return self.model()

    def set_current_row(self, row: int) -> None:
        row = max(0, min(row, self._block_model.rowCount() - 1))
        if row < 0:
            return
        self._block_model.set_current_row(row)
        self._center_current_row()
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
        self._center_current_row()

    def _on_clicked(self, index: QModelIndex) -> None:
        self.set_current_row(index.row())

    def _resize_rows(self) -> None:
        self.resizeRowsToContents()
        self._center_current_row()

    def _center_current_row(self) -> None:
        if self._block_model.rowCount() > 0:
            self.scrollTo(self._block_model.index(self._block_model.current_row, 0), QAbstractItemView.PositionAtCenter)
