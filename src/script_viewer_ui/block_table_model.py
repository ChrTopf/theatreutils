from typing import Any, Optional

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor, QFont

from block import Block
from script_viewer_ui import theme

COLUMNS = ("Mic", "Audio", "Light", "Character", "Text")
MIC_COLUMN = COLUMNS.index("Mic")
AUDIO_COLUMN = COLUMNS.index("Audio")
LIGHT_COLUMN = COLUMNS.index("Light")
CHARACTER_COLUMN = COLUMNS.index("Character")
TEXT_COLUMN = COLUMNS.index("Text")

# Custom roles exposing the whole Block of a row and whether it is the current one, e.g. to the MicCueDelegate.
BLOCK_ROLE = Qt.UserRole + 1
IS_CURRENT_ROLE = Qt.UserRole + 2


class BlockTableModel(QAbstractTableModel):
    """Presents the blocks as read-only table rows and keeps track of the current block.

    The current block is highlighted, all other blocks are dimmed. Changing the
    current block only restyles the two affected rows.
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

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(COLUMNS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return COLUMNS[section]
        return None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        block = self._blocks[index.row()]
        is_current = index.row() == self._current_row

        if role == Qt.DisplayRole:
            return self._display_text(block, index.column())
        if role == Qt.ForegroundRole:
            return self._foreground(block, index.column(), is_current)
        if role == Qt.BackgroundRole:
            return theme.CURRENT_BACKGROUND if is_current else theme.BACKGROUND
        if role == Qt.FontRole:
            return self._font(block, index.column())
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignLeft | Qt.AlignTop)
        if role == BLOCK_ROLE:
            return block
        if role == IS_CURRENT_ROLE:
            return is_current
        return None

    def _emit_row_changed(self, row: int) -> None:
        if 0 <= row < len(self._blocks):
            self.dataChanged.emit(self.index(row, 0), self.index(row, len(COLUMNS) - 1))

    @staticmethod
    def _display_text(block: Block, column: int) -> Optional[str]:
        if column == AUDIO_COLUMN:
            return block.audio_effect
        if column == LIGHT_COLUMN:
            return block.light
        if column == CHARACTER_COLUMN:
            return block.character
        if column == TEXT_COLUMN:
            if block.direction:
                return f"({block.direction}) {block.text}"
            return block.text
        # The mic column is painted by the MicCueDelegate.
        return None

    @staticmethod
    def _foreground(block: Block, column: int, is_current: bool) -> QColor:
        if column == AUDIO_COLUMN:
            return theme.AUDIO_EFFECT if is_current else theme.DIMMED_AUDIO_EFFECT
        if column == LIGHT_COLUMN:
            return theme.LIGHT if is_current else theme.DIMMED_LIGHT
        if block.type == "command":
            return theme.COMMAND_TEXT if is_current else theme.DIMMED_COMMAND_TEXT
        return theme.TEXT if is_current else theme.DIMMED_TEXT

    @staticmethod
    def _font(block: Block, column: int) -> QFont:
        font = QFont()
        font.setPointSize(theme.FONT_POINT_SIZE)
        if column == CHARACTER_COLUMN or block.type == "command":
            font.setBold(True)
        if column == TEXT_COLUMN and block.type == "acting":
            font.setItalic(True)
        return font
