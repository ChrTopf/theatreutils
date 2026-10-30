from dataclasses import dataclass
from PyQt5.QtGui import QColor

@dataclass(frozen=True, eq=False)
class CueLane:
    """A column running down the page next to the block cards, showing the cues of one deck."""
    name: str
    prefix: str
    color: QColor
