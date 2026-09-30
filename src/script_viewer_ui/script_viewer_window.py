from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

from block import Block
from script_viewer_ui import theme
from script_viewer_ui.block_table_model import BlockTableModel
from script_viewer_ui.block_table_view import BlockTableView


class ScriptViewerWindow(QMainWindow):
    """Main window of the Script Viewer: a status line above the block table.

    The status line shows where in the show the current block is located, so
    the position can be told at a glance while following the performance.
    """

    def __init__(self, blocks: list[Block], title: str):
        super().__init__()
        self.setWindowTitle(f"Script Viewer - {title}")
        self._blocks = blocks

        self._status_label = QLabel()
        status_font = QFont()
        status_font.setPointSize(theme.FONT_POINT_SIZE)
        status_font.setBold(True)
        self._status_label.setFont(status_font)
        self._status_label.setStyleSheet(f"color: {theme.TEXT.name()}; padding: 6px;")

        self._table = BlockTableView(BlockTableModel(blocks, self))
        self._table.current_row_changed.connect(self._update_status)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._status_label)
        layout.addWidget(self._table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet(f"background-color: {theme.BACKGROUND.name()};")
        self.setCentralWidget(central_widget)

        self._table.setFocus()
        self._update_status(0)

    def _update_status(self, row: int) -> None:
        if not self._blocks:
            self._status_label.setText("No blocks found in the workbook.")
            return
        block = self._blocks[row]
        self._status_label.setText(
            f"{block.part}  ·  Scene {block.scene}  ·  Page {block.page}  ·  Block {row + 1} / {len(self._blocks)}"
        )
