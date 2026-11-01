from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QSlider,
                             QSpinBox, QVBoxLayout)

from script_viewer_ui import theme
from script_viewer_ui.viewer_settings import (MAX_LANE_WIDTH, MIN_LANE_WIDTH, POSITION_BOTTOM, POSITION_TOP,
                                              SETTINGS_PATH, ViewerSettings)

LANE_WIDTH_STEP = 10
POSITION_TICK_INTERVAL = 25
POSITION_LABEL_WIDTH = 70


class SettingsDialog(QDialog):
    """Edits the ViewerSettings. Saving and applying them is left to the caller once the dialog is accepted."""

    def __init__(self, settings: ViewerSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Script Viewer Settings")

        self._lane_width_box = QSpinBox()
        self._lane_width_box.setRange(MIN_LANE_WIDTH, MAX_LANE_WIDTH)
        self._lane_width_box.setSingleStep(LANE_WIDTH_STEP)
        self._lane_width_box.setSuffix(" px")
        self._lane_width_box.setValue(settings.lane_width)

        self._position_slider = QSlider(Qt.Horizontal)
        self._position_slider.setRange(POSITION_TOP, POSITION_BOTTOM)
        self._position_slider.setTickPosition(QSlider.TicksBelow)
        self._position_slider.setTickInterval(POSITION_TICK_INTERVAL)
        self._position_label = QLabel()
        self._position_label.setMinimumWidth(POSITION_LABEL_WIDTH)
        self._position_slider.valueChanged.connect(self._show_position)
        self._position_slider.setValue(settings.current_block_position)
        self._show_position(settings.current_block_position)

        self._lane_letter_prefixes_box = QCheckBox("Label the cues with the letter of their lane (L, S, Q) instead of #")
        self._lane_letter_prefixes_box.setChecked(settings.lane_letter_prefixes)
        self._mutes_in_lisp_lane_box = QCheckBox("Show the X32 mutes and unmutes in the LiSP Cues lane as well")
        self._mutes_in_lisp_lane_box.setChecked(settings.mutes_in_lisp_lane)

        position_row = QHBoxLayout()
        position_row.addWidget(self._position_slider)
        position_row.addWidget(self._position_label)

        form = QFormLayout()
        form.addRow("Cue lane width", self._lane_width_box)
        form.addRow("Current block position", position_row)
        form.addRow(self._lane_letter_prefixes_box)
        form.addRow(self._mutes_in_lisp_lane_box)

        path_label = QLabel(f"Saved to {SETTINGS_PATH}")
        path_label.setObjectName("settingsPath")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(path_label)
        layout.addWidget(buttons)
        self.setStyleSheet(_STYLE_SHEET)

    def settings(self) -> ViewerSettings:
        return ViewerSettings(
            lane_width=self._lane_width_box.value(),
            mutes_in_lisp_lane=self._mutes_in_lisp_lane_box.isChecked(),
            lane_letter_prefixes=self._lane_letter_prefixes_box.isChecked(),
            current_block_position=self._position_slider.value(),
        )

    def _show_position(self, position: int) -> None:
        self._position_label.setText(_position_text(position))


def _position_text(position: int) -> str:
    if position == POSITION_TOP:
        return "Top"
    if position == POSITION_BOTTOM:
        return "Bottom"
    if position == (POSITION_TOP + POSITION_BOTTOM) // 2:
        return "Center"
    return f"{position} %"


_STYLE_SHEET = f"""
QDialog {{
    background-color: {theme.BAR.name()};
}}
QLabel, QCheckBox {{
    color: {theme.TEXT.name()};
    font-size: {theme.STATUS_POINT_SIZE}pt;
}}
QLabel#settingsPath {{
    color: {theme.MUTED_LABEL.name()};
}}
QSpinBox, QPushButton {{
    background-color: {theme.PAGE.name()};
    color: {theme.TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: {theme.STATUS_POINT_SIZE}pt;
}}
QPushButton {{
    min-width: 70px;
}}
"""
