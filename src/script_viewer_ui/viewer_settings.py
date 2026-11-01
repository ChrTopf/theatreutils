import json
import os
from dataclasses import asdict, dataclass, fields

from script_viewer_ui import theme

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".theatreutils", "script_viewer.json")

MIN_LANE_WIDTH = 150
MAX_LANE_WIDTH = 600

POSITION_TOP = 0
POSITION_BOTTOM = 100

# LiSP's default OSC input port.
DEFAULT_LISP_HOST = "127.0.0.1"
DEFAULT_LISP_PORT = 9000
MIN_PORT = 1
MAX_PORT = 65535

DEFAULT_GO_BUTTON_PORT = "/dev/ttyACM0"
DEFAULT_GO_BUTTON_BAUD_RATE = 9600
MIN_BAUD_RATE = 300
MAX_BAUD_RATE = 2000000


@dataclass
class ViewerSettings:
    """The preferences of the Script Viewer, kept in a JSON file in the home directory of the user."""

    lane_width: int = theme.LANE_WIDTH
    mutes_in_lisp_lane: bool = False
    lane_letter_prefixes: bool = True
    current_block_position: int = POSITION_TOP
    show_lisp_lane: bool = True
    show_x32_lane: bool = False
    show_light_cue_lane: bool = False
    lisp_sync: bool = False
    lisp_host: str = DEFAULT_LISP_HOST
    lisp_port: int = DEFAULT_LISP_PORT
    go_on_return: bool = False
    physical_go_button: bool = False
    go_button_port: str = DEFAULT_GO_BUTTON_PORT
    go_button_baud_rate: int = DEFAULT_GO_BUTTON_BAUD_RATE

    @classmethod
    def load(cls, path: str = SETTINGS_PATH) -> "ViewerSettings":
        """Reads the settings. A missing file, or a missing or invalid value, falls back to the default."""
        settings = cls()
        try:
            with open(path, "r", encoding="utf-8") as settings_file:
                data = json.load(settings_file)
        except (OSError, ValueError):
            return settings
        if not isinstance(data, dict):
            return settings

        for setting in fields(cls):
            value = data.get(setting.name)
            # Compared exactly, so a bool is not taken for an int.
            if type(value) is type(getattr(settings, setting.name)):
                setattr(settings, setting.name, value)
        settings.lane_width = _clamp(settings.lane_width, MIN_LANE_WIDTH, MAX_LANE_WIDTH)
        settings.current_block_position = _clamp(settings.current_block_position, POSITION_TOP, POSITION_BOTTOM)
        settings.lisp_host = settings.lisp_host.strip() or DEFAULT_LISP_HOST
        if not MIN_PORT <= settings.lisp_port <= MAX_PORT:
            settings.lisp_port = DEFAULT_LISP_PORT
        settings.go_button_port = settings.go_button_port.strip() or DEFAULT_GO_BUTTON_PORT
        if not MIN_BAUD_RATE <= settings.go_button_baud_rate <= MAX_BAUD_RATE:
            settings.go_button_baud_rate = DEFAULT_GO_BUTTON_BAUD_RATE
        return settings

    def save(self, path: str = SETTINGS_PATH) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as settings_file:
            json.dump(asdict(self), settings_file, indent=4)


def _clamp(value: int, lowest: int, highest: int) -> int:
    return max(lowest, min(value, highest))
