from typing import Any

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt

from model.block import Block

# Custom roles exposing the whole Block of a row and whether it is the current one to the BlockDelegate.
BLOCK_ROLE = Qt.UserRole + 1
IS_CURRENT_ROLE = Qt.UserRole + 2


class BlockListModel(QAbstractListModel):
    """Presents the blocks as the read-only rows of a document and keeps track of the current block.

    Every row is painted as a whole by the BlockDelegate, so the model only
    hands out the Block itself instead of per column strings. Changing the
    current block only repaints the two affected rows.
    """

    def __init__(self, blocks: list[Block], parent=None):
        super().__init__(parent)
        self._blocks = blocks
        self._current_row = 0

    @property
    def current_row(self) -> int:
        return self._current_row

    def set_current_row(self, row: int) -> None:
        if row == self._current_row:
            return
        previous_row = self._current_row
        self._current_row = row
        self._emit_row_changed(previous_row)
        self._emit_row_changed(row)

    def block_at(self, row: int) -> Block:
        return self._blocks[row]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._blocks)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        if role == BLOCK_ROLE:
            return self._blocks[index.row()]
        if role == IS_CURRENT_ROLE:
            return index.row() == self._current_row
        return None

    def _emit_row_changed(self, row: int) -> None:
        if 0 <= row < len(self._blocks):
            index = self.index(row)
            self.dataChanged.emit(index, index)
