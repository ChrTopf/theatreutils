from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from script_viewer_ui import theme
from script_viewer_ui.cue_segment import CueSegment

NO_CUE = "—"
BLINK_PROPERTY = "blink"
CUE_DISPLAY_SPACING = 32


class LispBar(QWidget):
    """The bar below the document with the last and next LiSP cue and the GO button triggering the next one."""

    go_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_cue_label = QLabel(NO_CUE)
        self._next_cue_label = QLabel(NO_CUE)

        self._go_button = QPushButton("GO")
        self._go_button.setObjectName("goButton")
        self._go_button.setFocusPolicy(Qt.NoFocus)
        self._go_button.setFixedSize(theme.GO_BUTTON_WIDTH, theme.GO_BUTTON_HEIGHT)
        self._go_button.setToolTip("Start the next LiSP cue")
        self._go_button.clicked.connect(self.go_pressed)
        self._go_button.setEnabled(False)

        self._blink_timer = QTimer(self, interval=theme.GO_BLINK_INTERVAL_MS)
        self._blink_timer.timeout.connect(self._toggle_blink)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(theme.PAGE_MARGIN, 8, theme.PAGE_MARGIN, 8)
        layout.setSpacing(CUE_DISPLAY_SPACING)
        layout.addStretch()
        layout.addLayout(self._cue_display("Last LiSP cue", self._last_cue_label))
        layout.addLayout(self._cue_display("Next LiSP cue", self._next_cue_label))
        layout.addWidget(self._go_button)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(_STYLE_SHEET)

    def set_armed(self, armed: bool) -> None:
        if armed == self._go_button.isEnabled():
            return
        self._go_button.setEnabled(armed)
        if armed:
            self._blink_timer.start()
        else:
            self._blink_timer.stop()
            self._set_blink(False)

    def press_go(self) -> None:
        self._go_button.click()

    def show_last_cue(self, segment: CueSegment | None) -> None:
        self._show_cue(self._last_cue_label, segment)

    def show_next_cue(self, segment: CueSegment | None) -> None:
        self._show_cue(self._next_cue_label, segment)

    @staticmethod
    def _cue_display(caption_text: str, cue_label: QLabel) -> QVBoxLayout:
        caption = QLabel(caption_text)
        caption.setObjectName("cueCaption")
        cue_label.setObjectName("cue")
        display = QVBoxLayout()
        display.setSpacing(2)
        display.addWidget(caption)
        display.addWidget(cue_label)
        return display

    @staticmethod
    def _show_cue(label: QLabel, segment: CueSegment | None) -> None:
        label.setText(f"{segment.label}  {segment.name}" if segment else NO_CUE)
        color = segment.color if segment else theme.MUTED_LABEL
        label.setStyleSheet(f"color: {color.name()};")

    def _toggle_blink(self) -> None:
        self._set_blink(not self._go_button.property(BLINK_PROPERTY))

    def _set_blink(self, on: bool) -> None:
        self._go_button.setProperty(BLINK_PROPERTY, on)
        # Style sheet rules depending on a property only apply once the widget is polished again.
        self._go_button.style().unpolish(self._go_button)
        self._go_button.style().polish(self._go_button)


_STYLE_SHEET = f"""
LispBar {{
    background-color: {theme.BAR.name()};
    border-top: 1px solid {theme.BAR_BORDER.name()};
}}
QLabel#cueCaption {{
    color: {theme.MUTED_LABEL.name()};
    font-size: {theme.STATUS_POINT_SIZE}pt;
}}
QLabel#cue {{
    font-size: {theme.LISP_CUE_POINT_SIZE}pt;
    font-weight: bold;
}}
QPushButton#goButton {{
    background-color: {theme.PAGE.name()};
    color: {theme.DIMMED_TEXT.name()};
    border: 2px solid {theme.BAR_BORDER.name()};
    border-radius: 8px;
    font-size: {theme.GO_POINT_SIZE}pt;
    font-weight: bold;
}}
QPushButton#goButton:enabled {{
    background-color: {theme.GO_ARMED.name()};
    color: {theme.GO_ARMED_TEXT.name()};
    border-color: {theme.GO_ARMED_BLINK.name()};
}}
QPushButton#goButton[blink="true"]:enabled {{
    background-color: {theme.GO_ARMED_BLINK.name()};
}}
"""
