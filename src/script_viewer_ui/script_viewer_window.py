from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from model.block import Block
from script_viewer_ui import theme
from script_viewer_ui.block_list_model import BlockListModel
from script_viewer_ui.block_list_view import BlockListView
from script_viewer_ui.scene_index import SceneIndex
from script_viewer_ui.scene_jump_bar import SceneJumpBar


class ScriptViewerWindow(QMainWindow):
    """Main window of the Script Viewer: the scene jump bar above the script document.

    The bar tells where in the show the current block is located and jumps to
    any scene of any part, so the position can be read and changed at a glance
    while following the performance.
    """

    def __init__(self, blocks: list[Block], title: str):
        super().__init__()
        self.setWindowTitle(f"Script Viewer - {title}")
        self._blocks = blocks

        self._jump_bar = SceneJumpBar(SceneIndex(blocks), len(blocks))
        self._view = BlockListView(BlockListModel(blocks, self))
        self._jump_bar.scene_selected.connect(self._jump_to_row)
        self._view.current_row_changed.connect(self._update_position)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._jump_bar)
        layout.addWidget(self._view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet(f"background-color: {theme.PAGE.name()};")
        self.setCentralWidget(central_widget)

        self._view.setFocus()
        self._update_position(0)

    def _jump_to_row(self, row: int) -> None:
        self._view.set_current_row(row)
        # The document keeps the keyboard, so the arrow keys work right after a jump.
        self._view.setFocus()

    def _update_position(self, row: int) -> None:
        if not self._blocks:
            self._jump_bar.show_empty_script()
            return
        self._jump_bar.show_current_block(row, self._blocks[row])
