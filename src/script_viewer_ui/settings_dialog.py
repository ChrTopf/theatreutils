import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                             QLineEdit, QSlider, QSpinBox, QVBoxLayout, QWidget)

from script_viewer_ui import theme
from script_viewer_ui.cue_lane_segments import LIGHT_CUE_LANE, LISP_LANE, X32_LANE
from script_viewer_ui.viewer_settings import (DEFAULT_GO_BUTTON_PORT, DEFAULT_LISP_HOST, MAX_BAUD_RATE,
                                              MAX_LANE_WIDTH, MAX_PORT, MIN_BAUD_RATE, MIN_LANE_WIDTH, MIN_PORT,
                                              POSITION_BOTTOM, POSITION_TOP, SETTINGS_PATH, ViewerSettings)

LANE_WIDTH_STEP = 10
POSITION_LABEL_WIDTH = 80
COLUMN_SPACING = 20
SECTION_SPACING = 16
FIELD_MIN_WIDTH = 220
# Style sheets need forward slashes, also on Windows.
CHECK_ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "check.svg").replace(os.sep, "/")


class SettingsDialog(QDialog):
    """Edits the ViewerSettings. Saving and applying them is left to the caller once the dialog is accepted."""

    def __init__(self, settings: ViewerSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Script Viewer Settings")

        # Cue lanes
        self._show_lisp_lane_box = QCheckBox(LISP_LANE.name)
        self._show_lisp_lane_box.setChecked(settings.show_lisp_lane)
        self._show_x32_lane_box = QCheckBox(X32_LANE.name)
        self._show_x32_lane_box.setChecked(settings.show_x32_lane)
        self._show_light_cue_lane_box = QCheckBox(LIGHT_CUE_LANE.name)
        self._show_light_cue_lane_box.setChecked(settings.show_light_cue_lane)
        self._lane_width_box = QSpinBox()
        self._lane_width_box.setRange(MIN_LANE_WIDTH, MAX_LANE_WIDTH)
        self._lane_width_box.setSingleStep(LANE_WIDTH_STEP)
        self._lane_width_box.setSuffix(" px")
        self._lane_width_box.setValue(settings.lane_width)
        self._lane_letter_prefixes_box = QCheckBox("Label the cues with their lane letter (L, S, Q) instead of #")
        self._lane_letter_prefixes_box.setChecked(settings.lane_letter_prefixes)
        self._mutes_in_lisp_lane_box = QCheckBox("Also show the X32 mutes and unmutes in the LiSP Cues lane")
        self._mutes_in_lisp_lane_box.setChecked(settings.mutes_in_lisp_lane)

        lanes_column = QVBoxLayout()
        lanes_column.setSpacing(6)
        for box in (self._show_lisp_lane_box, self._show_x32_lane_box, self._show_light_cue_lane_box):
            lanes_column.addWidget(box)
        lanes_form = _form()
        lanes_form.addRow("Shown lanes", lanes_column)
        lanes_form.addRow("Lane width", self._lane_width_box)
        lanes_form.addRow(self._lane_letter_prefixes_box)
        lanes_form.addRow(self._mutes_in_lisp_lane_box)

        # Document
        self._position_slider = QSlider(Qt.Horizontal)
        self._position_slider.setRange(POSITION_TOP, POSITION_BOTTOM)
        self._position_label = QLabel()
        self._position_label.setMinimumWidth(POSITION_LABEL_WIDTH)
        self._position_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._position_slider.valueChanged.connect(self._show_position)
        self._position_slider.setValue(settings.current_block_position)
        self._show_position(settings.current_block_position)

        position_row = QHBoxLayout()
        position_row.addWidget(self._position_slider)
        position_row.addWidget(self._position_label)
        document_form = _form()
        document_form.addRow("Current block position", position_row)
        document_form.addRow(_hint("Where the current block is kept within the view."))

        # LiSP synchronization
        self._lisp_sync_box = QCheckBox("Trigger the LiSP cues with the GO button of the Script Viewer")
        self._lisp_sync_box.setChecked(settings.lisp_sync)
        self._lisp_host_edit = QLineEdit(settings.lisp_host)
        self._lisp_host_edit.setPlaceholderText(DEFAULT_LISP_HOST)
        self._lisp_port_box = QSpinBox()
        self._lisp_port_box.setRange(MIN_PORT, MAX_PORT)
        self._lisp_port_box.setValue(settings.lisp_port)
        self._go_on_return_box = QCheckBox("Press the GO button with the Return key")
        self._go_on_return_box.setChecked(settings.go_on_return)

        self._lisp_form = _form()
        self._lisp_form.addRow(self._lisp_sync_box)
        self._lisp_form.addRow("Host", self._lisp_host_edit)
        self._lisp_form.addRow("OSC port", self._lisp_port_box)
        self._lisp_form.addRow(self._go_on_return_box)

        # Physical GO button
        self._physical_go_button_box = QCheckBox("Press the GO button with the Arduino buzzer")
        self._physical_go_button_box.setChecked(settings.physical_go_button)
        self._go_button_port_edit = QLineEdit(settings.go_button_port)
        self._go_button_port_edit.setPlaceholderText(DEFAULT_GO_BUTTON_PORT)
        self._go_button_baud_rate_box = QSpinBox()
        self._go_button_baud_rate_box.setRange(MIN_BAUD_RATE, MAX_BAUD_RATE)
        self._go_button_baud_rate_box.setValue(settings.go_button_baud_rate)

        self._go_button_form = _form()
        self._go_button_form.addRow(self._physical_go_button_box)
        self._go_button_form.addRow("Serial port", self._go_button_port_edit)
        self._go_button_form.addRow("Baud rate", self._go_button_baud_rate_box)
        self._go_button_form.addRow(_hint("Requires the LiSP synchronization."))

        self._lisp_sync_box.toggled.connect(self._update_enabled_widgets)
        self._physical_go_button_box.toggled.connect(self._update_enabled_widgets)
        self._update_enabled_widgets()

        display_column = QVBoxLayout()
        display_column.setSpacing(SECTION_SPACING)
        display_column.addWidget(_section("Cue lanes", lanes_form))
        display_column.addWidget(_section("Document", document_form))
        display_column.addStretch()

        control_column = QVBoxLayout()
        control_column.setSpacing(SECTION_SPACING)
        control_column.addWidget(_section("LiSP synchronization", self._lisp_form))
        control_column.addWidget(_section("Physical GO button", self._go_button_form))
        control_column.addStretch()

        columns = QHBoxLayout()
        columns.setSpacing(COLUMN_SPACING)
        columns.addLayout(display_column, 1)
        columns.addLayout(control_column, 1)

        path_label = QLabel(f"Saved to {SETTINGS_PATH}")
        path_label.setObjectName("hint")
        path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setObjectName("primaryButton")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        footer = QHBoxLayout()
        footer.addWidget(path_label)
        footer.addStretch()
        footer.addWidget(buttons)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(theme.PAGE_MARGIN, theme.PAGE_MARGIN, theme.PAGE_MARGIN, theme.PAGE_MARGIN)
        layout.setSpacing(SECTION_SPACING)
        layout.addLayout(columns)
        layout.addLayout(footer)
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

    def _update_enabled_widgets(self) -> None:
        # The GO button, and with it the physical GO button, only exists while synchronizing with LiSP.
        lisp_sync = self._lisp_sync_box.isChecked()
        serial_editable = lisp_sync and self._physical_go_button_box.isChecked()
        _set_enabled(self._lisp_form, (self._lisp_host_edit, self._lisp_port_box, self._go_on_return_box), lisp_sync)
        _set_enabled(self._go_button_form, (self._physical_go_button_box,), lisp_sync)
        _set_enabled(self._go_button_form, (self._go_button_port_edit, self._go_button_baud_rate_box), serial_editable)


def _form() -> QFormLayout:
    form = QFormLayout()
    form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
    form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    form.setHorizontalSpacing(16)
    form.setVerticalSpacing(10)
    return form


def _section(title: str, form: QFormLayout) -> QGroupBox:
    section = QGroupBox(title)
    section.setLayout(form)
    section.setMinimumWidth(FIELD_MIN_WIDTH * 2)
    return section


def _hint(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("hint")
    label.setWordWrap(True)
    return label


def _set_enabled(form: QFormLayout, fields: tuple[QWidget, ...], enabled: bool) -> None:
    """Enables the fields together with their labels in the form, so disabled rows are dimmed as a whole."""
    for field in fields:
        field.setEnabled(enabled)
        label = form.labelForField(field)
        if label is not None:
            label.setEnabled(enabled)


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
    font-size: {theme.SETTINGS_POINT_SIZE}pt;
}}
QLabel:disabled, QCheckBox:disabled {{
    color: {theme.DIMMED_TEXT.name()};
}}
QLabel#hint {{
    color: {theme.MUTED_LABEL.name()};
    font-size: {theme.SETTINGS_HINT_POINT_SIZE}pt;
}}

QGroupBox {{
    background-color: {theme.BLOCK.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 8px;
    margin-top: 18px;
    padding: 18px 14px 14px 14px;
    color: {theme.ACCENT.name()};
    font-size: {theme.SETTINGS_SECTION_POINT_SIZE}pt;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
}}

QCheckBox {{
    spacing: 10px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {theme.MUTED_LABEL.name()};
    border-radius: 4px;
    background-color: {theme.PAGE.name()};
}}
QCheckBox::indicator:hover {{
    border-color: {theme.ACCENT.name()};
}}
QCheckBox::indicator:checked {{
    border-color: {theme.ACCENT.name()};
    background-color: {theme.ACCENT.name()};
    image: url({CHECK_ICON_PATH});
}}
QCheckBox::indicator:disabled {{
    border-color: {theme.BAR_BORDER.name()};
    background-color: {theme.BAR.name()};
}}
QCheckBox::indicator:checked:disabled {{
    border-color: {theme.DIMMED_TEXT.name()};
    background-color: {theme.DIMMED_TEXT.name()};
}}

QSpinBox, QLineEdit {{
    background-color: {theme.PAGE.name()};
    color: {theme.TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 4px;
    padding: 6px 8px;
    min-width: {FIELD_MIN_WIDTH}px;
    font-size: {theme.SETTINGS_POINT_SIZE}pt;
    selection-background-color: {theme.ACCENT.name()};
    selection-color: {theme.PAGE.name()};
}}
QSpinBox:focus, QLineEdit:focus {{
    border-color: {theme.ACCENT.name()};
}}
QSpinBox:disabled, QLineEdit:disabled {{
    color: {theme.DIMMED_TEXT.name()};
    background-color: {theme.BAR.name()};
}}

QSlider::groove:horizontal {{
    height: 6px;
    background: {theme.BAR_BORDER.name()};
    border-radius: 3px;
}}
QSlider::sub-page:horizontal {{
    background: {theme.ACCENT.name()};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {theme.TEXT.name()};
    width: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QPushButton {{
    background-color: {theme.PAGE.name()};
    color: {theme.TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 6px;
    padding: 8px 20px;
    min-width: 90px;
    font-size: {theme.SETTINGS_POINT_SIZE}pt;
}}
QPushButton:hover {{
    border-color: {theme.ACCENT.name()};
}}
QPushButton#primaryButton {{
    background-color: {theme.ACCENT.name()};
    color: {theme.PAGE.name()};
    border-color: {theme.ACCENT.name()};
    font-weight: bold;
}}
"""
