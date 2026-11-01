from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QVBoxLayout, QWidget

from model.script import Script
from script_viewer_ui import theme
from script_viewer_ui.block_list_model import BlockListModel
from script_viewer_ui.block_list_view import BlockListView
from script_viewer_ui.cue_lane_segments import CueLaneSegments
from script_viewer_ui.scene_index import SceneIndex
from script_viewer_ui.top_bar import TopBar
from script_viewer_ui.settings_dialog import SettingsDialog
from script_viewer_ui.viewer_settings import SETTINGS_PATH, ViewerSettings


class ScriptViewerWindow(QMainWindow):
    """Main window of the Script Viewer"""

    def __init__(self, script: Script, title: str):
        super().__init__()
        self.setWindowTitle(f"Script Viewer - {title}")
        self._blocks = script.blocks
        self._settings = ViewerSettings.load()
        self._cue_lanes = CueLaneSegments(script, self._settings)

        self._top_bar = TopBar(SceneIndex(self._blocks), len(self._blocks))
        self._view = BlockListView(BlockListModel(self._blocks, self._cue_lanes, self), self._settings)
        self._top_bar.scene_selected.connect(self._jump_to_row)
        self._top_bar.settings_requested.connect(self._edit_settings)
        self._view.current_row_changed.connect(self._update_position)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._top_bar)
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

    def _edit_settings(self) -> None:
        dialog = SettingsDialog(self._settings, self)
        if dialog.exec_() == QDialog.Accepted:
            self._settings = dialog.settings()
            try:
                self._settings.save()
            except OSError as error:
                # The settings are still applied, they are only lost once the viewer is closed.
                QMessageBox.warning(self, "Settings not saved",
                                    f"The settings could not be saved to '{SETTINGS_PATH}': {error}")
            self._cue_lanes.apply_settings(self._settings)
            self._view.apply_settings(self._settings)
        self._view.setFocus()

    def _update_position(self, row: int) -> None:
        if not self._blocks:
            self._top_bar.show_empty_script()
            return
        self._top_bar.show_current_block(row, self._blocks[row])
