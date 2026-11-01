from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                             QLineEdit, QSlider, QSpinBox, QVBoxLayout)

from script_viewer_ui import theme
from script_viewer_ui.cue_lane_segments import LIGHT_CUE_LANE, LISP_LANE, X32_LANE
from script_viewer_ui.viewer_settings import (DEFAULT_GO_BUTTON_PORT, DEFAULT_LISP_HOST, MAX_BAUD_RATE,
                                              MAX_LANE_WIDTH, MAX_PORT, MIN_BAUD_RATE, MIN_LANE_WIDTH, MIN_PORT,
                                              POSITION_BOTTOM, POSITION_TOP, SETTINGS_PATH, ViewerSettings)

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

        self._show_lisp_lane_box = QCheckBox(LISP_LANE.name)
        self._show_lisp_lane_box.setChecked(settings.show_lisp_lane)
        self._show_x32_lane_box = QCheckBox(X32_LANE.name)
        self._show_x32_lane_box.setChecked(settings.show_x32_lane)
        self._show_light_cue_lane_box = QCheckBox(LIGHT_CUE_LANE.name)
        self._show_light_cue_lane_box.setChecked(settings.show_light_cue_lane)

        self._lisp_sync_box = QCheckBox("Trigger the LiSP cues with the GO button of the Script Viewer")
        self._lisp_sync_box.setChecked(settings.lisp_sync)
        self._lisp_host_edit = QLineEdit(settings.lisp_host)
        self._lisp_host_edit.setPlaceholderText(DEFAULT_LISP_HOST)
        self._lisp_port_box = QSpinBox()
        self._lisp_port_box.setRange(MIN_PORT, MAX_PORT)
        self._lisp_port_box.setValue(settings.lisp_port)
        self._go_on_return_box = QCheckBox("Press the GO button with the Return key")
        self._go_on_return_box.setChecked(settings.go_on_return)
        for widget in (self._lisp_host_edit, self._lisp_port_box, self._go_on_return_box):
            self._lisp_sync_box.toggled.connect(widget.setEnabled)
            widget.setEnabled(settings.lisp_sync)

        self._physical_go_button_box = QCheckBox("Press the GO button with the physical GO button (Arduino buzzer)")
        self._physical_go_button_box.setChecked(settings.physical_go_button)
        self._go_button_port_edit = QLineEdit(settings.go_button_port)
        self._go_button_port_edit.setPlaceholderText(DEFAULT_GO_BUTTON_PORT)
        self._go_button_baud_rate_box = QSpinBox()
        self._go_button_baud_rate_box.setRange(MIN_BAUD_RATE, MAX_BAUD_RATE)
        self._go_button_baud_rate_box.setValue(settings.go_button_baud_rate)
        self._lisp_sync_box.toggled.connect(self._update_physical_go_button_widgets)
        self._physical_go_button_box.toggled.connect(self._update_physical_go_button_widgets)
        self._update_physical_go_button_widgets()

        go_button_form = QFormLayout()
        go_button_form.addRow(self._physical_go_button_box)
        go_button_form.addRow("Serial port", self._go_button_port_edit)
        go_button_form.addRow("Baud rate", self._go_button_baud_rate_box)
        go_button_group = QGroupBox("Physical GO button")
        go_button_group.setLayout(go_button_form)

        lisp_address_row = QHBoxLayout()
        lisp_address_row.addWidget(self._lisp_host_edit)
        lisp_address_row.addWidget(QLabel("Port"))
        lisp_address_row.addWidget(self._lisp_port_box)

        lanes_row = QHBoxLayout()
        lanes_row.addWidget(self._show_lisp_lane_box)
        lanes_row.addWidget(self._show_x32_lane_box)
        lanes_row.addWidget(self._show_light_cue_lane_box)
        lanes_row.addStretch()

        position_row = QHBoxLayout()
        position_row.addWidget(self._position_slider)
        position_row.addWidget(self._position_label)

        form = QFormLayout()
        form.addRow("Shown cue lanes", lanes_row)
        form.addRow("Cue lane width", self._lane_width_box)
        form.addRow("Current block position", position_row)
        form.addRow(self._lane_letter_prefixes_box)
        form.addRow(self._mutes_in_lisp_lane_box)
        form.addRow("LiSP synchronization", self._lisp_sync_box)
        form.addRow("LiSP OSC address", lisp_address_row)
        form.addRow("", self._go_on_return_box)

        path_label = QLabel(f"Saved to {SETTINGS_PATH}")
        path_label.setObjectName("settingsPath")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(go_button_group)
        layout.addWidget(path_label)
        layout.addWidget(buttons)
        self.setStyleSheet(_STYLE_SHEET)

    def settings(self) -> ViewerSettings:
        return ViewerSettings(
            lane_width=self._lane_width_box.value(),
            mutes_in_lisp_lane=self._mutes_in_lisp_lane_box.isChecked(),
            lane_letter_prefixes=self._lane_letter_prefixes_box.isChecked(),
            current_block_position=self._position_slider.value(),
            show_lisp_lane=self._show_lisp_lane_box.isChecked(),
            show_x32_lane=self._show_x32_lane_box.isChecked(),
            show_light_cue_lane=self._show_light_cue_lane_box.isChecked(),
            lisp_sync=self._lisp_sync_box.isChecked(),
            lisp_host=self._lisp_host_edit.text().strip() or DEFAULT_LISP_HOST,
            lisp_port=self._lisp_port_box.value(),
            go_on_return=self._go_on_return_box.isChecked(),
            physical_go_button=self._physical_go_button_box.isChecked(),
            go_button_port=self._go_button_port_edit.text().strip() or DEFAULT_GO_BUTTON_PORT,
            go_button_baud_rate=self._go_button_baud_rate_box.value(),
        )

    def _show_position(self, position: int) -> None:
        self._position_label.setText(_position_text(position))

    def _update_physical_go_button_widgets(self) -> None:
        lisp_sync = self._lisp_sync_box.isChecked()
        self._physical_go_button_box.setEnabled(lisp_sync)
        serial_editable = lisp_sync and self._physical_go_button_box.isChecked()
        self._go_button_port_edit.setEnabled(serial_editable)
        self._go_button_baud_rate_box.setEnabled(serial_editable)


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
QGroupBox {{
    color: {theme.TEXT.name()};
    font-size: {theme.STATUS_POINT_SIZE}pt;
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 8px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}}
QLabel#settingsPath {{
    color: {theme.MUTED_LABEL.name()};
}}
QSpinBox, QLineEdit, QPushButton {{
    background-color: {theme.PAGE.name()};
    color: {theme.TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: {theme.STATUS_POINT_SIZE}pt;
}}
QSpinBox:disabled, QLineEdit:disabled, QCheckBox:disabled {{
    color: {theme.DIMMED_TEXT.name()};
}}
QPushButton {{
    min-width: 70px;
}}
"""
