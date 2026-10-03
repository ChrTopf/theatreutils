from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget

from model.block import Block
from script_viewer_ui import theme
from script_viewer_ui.scene_index import SceneIndex


class SceneJumpBar(QWidget):
    """The bar above the document: jump to a scene of a part, and the current position.

    Picking a part jumps to its first scene, picking a scene jumps to its first
    block. Both selectors also follow along while the show is being read, so
    they always show where the current block is located.
    """

    scene_selected = pyqtSignal(int)

    def __init__(self, index: SceneIndex, block_count: int, parent=None):
        super().__init__(parent)
        self._index = index
        self._block_count = block_count
        # Guards the selectors against emitting jumps while they are being synchronized.
        self._synchronizing = True

        self._part_box = QComboBox()
        self._scene_box = QComboBox()
        self._position_label = QLabel()
        self._position_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._part_box.currentIndexChanged.connect(self._on_part_changed)
        self._scene_box.currentIndexChanged.connect(self._on_scene_changed)
        self._part_box.addItems(index.parts())
        self._synchronizing = False

        enabled = block_count > 0
        self._part_box.setEnabled(enabled)
        self._scene_box.setEnabled(enabled)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(theme.PAGE_MARGIN, 8, theme.PAGE_MARGIN, 8)
        layout.setSpacing(8)
        layout.addWidget(QLabel("Part"))
        layout.addWidget(self._part_box)
        layout.addSpacing(8)
        layout.addWidget(QLabel("Scene"))
        layout.addWidget(self._scene_box)
        layout.addStretch()
        layout.addWidget(self._position_label)

        self.setStyleSheet(_STYLE_SHEET)

    def show_current_block(self, row: int, block: Block) -> None:
        """Moves the selectors onto the part and scene of the given block, without jumping."""
        self._synchronizing = True
        try:
            part_index = self._part_box.findText(block.part)
            if part_index >= 0:
                self._part_box.setCurrentIndex(part_index)
            scene_index = self._scene_box.findData(block.scene)
            if scene_index >= 0:
                self._scene_box.setCurrentIndex(scene_index)
        finally:
            self._synchronizing = False
        self._position_label.setText(f"Page {block.page}  ·  Block {row + 1} / {self._block_count}")

    def show_empty_script(self) -> None:
        self._position_label.setText("No blocks found in the workbook.")

    def _on_part_changed(self, part_index: int) -> None:
        self._fill_scenes(self._part_box.itemText(part_index))
        if not self._synchronizing:
            self._emit_selected_scene()

    def _on_scene_changed(self, _scene_index: int) -> None:
        if not self._synchronizing:
            self._emit_selected_scene()

    def _fill_scenes(self, part: str) -> None:
        # Filling the box must not look like the user picked the first scene.
        self._scene_box.blockSignals(True)
        self._scene_box.clear()
        for scene in self._index.scenes(part):
            self._scene_box.addItem(f"Scene {scene}", scene)
        self._scene_box.blockSignals(False)

    def _emit_selected_scene(self) -> None:
        row = self._index.first_row_of(self._part_box.currentText(), self._scene_box.currentData())
        if row is not None:
            self.scene_selected.emit(row)


_STYLE_SHEET = f"""
SceneJumpBar {{
    background-color: {theme.BAR.name()};
    border-bottom: 1px solid {theme.BAR_BORDER.name()};
}}
QLabel {{
    color: {theme.MUTED_LABEL.name()};
    font-size: {theme.STATUS_POINT_SIZE}pt;
}}
QComboBox {{
    background-color: {theme.PAGE.name()};
    color: {theme.TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 4px;
    padding: 4px 8px;
    min-width: 130px;
    font-size: {theme.STATUS_POINT_SIZE}pt;
}}
QComboBox:disabled {{
    color: {theme.DIMMED_TEXT.name()};
}}
QComboBox::drop-down {{
    border: none;
    width: 18px;
}}
QComboBox QAbstractItemView {{
    background-color: {theme.BLOCK.name()};
    color: {theme.TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    selection-background-color: {theme.CURRENT_BLOCK.name()};
    selection-color: {theme.TEXT.name()};
    outline: none;
}}
"""
