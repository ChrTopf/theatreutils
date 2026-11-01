from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QVBoxLayout, QWidget

from model.script import Script
from script_viewer_ui import theme
from script_viewer_ui.block_list_model import BlockListModel
from script_viewer_ui.block_list_view import BlockListView
from script_viewer_ui.cue_lane_segments import LISP_LANE, CueLaneSegments
from script_viewer_ui.cue_segment import CueSegment
from script_viewer_ui.go_button_listener import GoButtonListener
from script_viewer_ui.lisp_bar import LispBar
from script_viewer_ui.lisp_trigger import LispTrigger
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
        self._current_row = 0
        self._last_lisp_row: int | None = None
        self._lisp_trigger = LispTrigger()
        self._go_button_listener: GoButtonListener | None = None

        self._top_bar = TopBar(SceneIndex(self._blocks), len(self._blocks))
        self._view = BlockListView(BlockListModel(self._blocks, self._cue_lanes, self), self._settings)
        self._lisp_bar = LispBar()
        self._top_bar.scene_selected.connect(self._jump_to_row)
        self._top_bar.settings_requested.connect(self._edit_settings)
        self._view.current_row_changed.connect(self._update_position)
        self._lisp_bar.go_pressed.connect(self._trigger_lisp_cue)
        self._view.return_pressed.connect(self._go_on_return)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._top_bar)
        layout.addWidget(self._view)
        layout.addWidget(self._lisp_bar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet(f"background-color: {theme.PAGE.name()};")
        self.setCentralWidget(central_widget)

        self._view.setFocus()
        self._update_position(0)
        self._update_lisp_bar()
        self._update_go_button_listener()

    def closeEvent(self, event) -> None:
        self._stop_go_button_listener()
        super().closeEvent(event)

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
            self._update_lisp_bar()
            self._update_go_button_listener()
        self._view.setFocus()

    def _update_position(self, row: int) -> None:
        self._current_row = row
        self._update_go_button()
        if not self._blocks:
            self._top_bar.show_empty_script()
            return
        self._top_bar.show_current_block(row, self._blocks[row])

    def _go_on_return(self) -> None:
        if self._settings.lisp_sync and self._settings.go_on_return:
            self._lisp_bar.press_go()

    def _update_go_button_listener(self) -> None:
        """Starts, restarts or stops listening to the physical GO button according to the settings."""
        wanted = self._settings.lisp_sync and self._settings.physical_go_button
        listener = self._go_button_listener
        if (wanted and listener is not None and listener.isRunning()
                and listener.port == self._settings.go_button_port
                and listener.baud_rate == self._settings.go_button_baud_rate):
            return
        self._stop_go_button_listener()
        if wanted:
            listener = GoButtonListener(self._settings.go_button_port, self._settings.go_button_baud_rate, self)
            listener.pressed.connect(self._lisp_bar.press_go)
            listener.failed.connect(self._show_go_button_error)
            listener.start()
            self._go_button_listener = listener

    def _stop_go_button_listener(self) -> None:
        if self._go_button_listener is not None:
            self._go_button_listener.stop()
            self._go_button_listener = None

    def _show_go_button_error(self, error: str) -> None:
        QMessageBox.warning(self, "Physical GO button not available",
                            f"Cannot listen to the physical GO button on {self._settings.go_button_port} at "
                            f"{self._settings.go_button_baud_rate} baud: {error}\n\n"
                            f"Check the connection and confirm the settings again to retry.")
        self._view.setFocus()

    def _trigger_lisp_cue(self) -> None:
        segment = self._next_lisp_segment()
        if segment is None:
            return
        cue_number = self._cue_lanes.lisp_cue_number(segment.first_row)
        try:
            self._lisp_trigger.trigger(self._settings.lisp_host, self._settings.lisp_port, cue_number)
        except OSError as error:
            QMessageBox.warning(self, "LiSP cue not triggered",
                                f"The cue could not be sent to LiSP at "
                                f"{self._settings.lisp_host}:{self._settings.lisp_port}: {error}")
            self._view.setFocus()
            return
        self._last_lisp_row = segment.first_row
        self._update_lisp_bar()

    def _update_lisp_bar(self) -> None:
        self._lisp_bar.setVisible(self._settings.lisp_sync)
        last_segment = None
        if self._last_lisp_row is not None:
            last_segment = self._cue_lanes.segment_at(LISP_LANE, self._last_lisp_row)
        self._lisp_bar.show_last_cue(last_segment)
        self._update_go_button()

    def _update_go_button(self) -> None:
        next_segment = self._next_lisp_segment()
        self._lisp_bar.show_next_cue(next_segment)
        self._lisp_bar.set_armed(self._settings.lisp_sync and next_segment is not None)

    def _next_lisp_segment(self) -> CueSegment | None:
        segment = self._cue_lanes.segment_at(LISP_LANE, self._current_row)
        if segment is None or segment.first_row == self._last_lisp_row:
            return None
        return segment
