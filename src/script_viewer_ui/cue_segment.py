from dataclasses import dataclass
from PyQt5.QtGui import QColor

@dataclass(frozen=True)
class CueSegment:
    """The rows a cue stays active for: from the block triggering it up to the block triggering the next cue.

    If a block triggers several cues of the same deck at once, they share one
    segment and all of their names are listed.
    """

    first_row: int
    last_row: int
    names: tuple[str, ...]
    color: QColor

    def contains(self, row: int) -> bool:
        return self.first_row <= row <= self.last_row