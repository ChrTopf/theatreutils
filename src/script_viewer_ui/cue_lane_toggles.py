from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from script_viewer_ui import theme
from script_viewer_ui.cue_lanes import LANES, CueLane


class CueLaneToggles(QWidget):
    """One button per cue lane, showing or hiding that lane. All lanes start out visible.

    A shown lane's button is outlined in the color of the lane, a hidden lane's
    button is grey. The buttons never take the keyboard focus, so the arrow
    keys keep moving through the script after a click.
    """

    visible_lanes_changed = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: dict[CueLane, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        for lane in LANES:
            button = QPushButton(lane.name)
            button.setCheckable(True)
            button.setChecked(True)
            button.setFocusPolicy(Qt.NoFocus)
            button.setToolTip(f"Show or hide the {lane.name} lane")
            button.setStyleSheet(_button_style_sheet(lane))
            button.toggled.connect(self._emit_visible_lanes)
            self._buttons[lane] = button
            layout.addWidget(button)

    def visible_lanes(self) -> tuple[CueLane, ...]:
        return tuple(lane for lane in LANES if self._buttons[lane].isChecked())

    def _emit_visible_lanes(self) -> None:
        self.visible_lanes_changed.emit(self.visible_lanes())


def _button_style_sheet(lane: CueLane) -> str:
    return f"""
QPushButton {{
    background-color: {theme.PAGE.name()};
    color: {theme.DIMMED_TEXT.name()};
    border: 1px solid {theme.BAR_BORDER.name()};
    border-radius: 4px;
    padding: 4px 10px;
    font-size: {theme.STATUS_POINT_SIZE}pt;
    font-weight: bold;
}}
QPushButton:checked {{
    color: {lane.color.name()};
    border-color: {lane.color.name()};
}}
"""
