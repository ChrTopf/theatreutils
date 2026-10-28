from dataclasses import dataclass

from PyQt5.QtGui import QColor

from model.script import Script
from script_viewer_ui import theme


@dataclass(frozen=True, eq=False)
class CueLane:
    """A column running down the page next to the block cards, showing the cues of one deck."""

    name: str
    color: QColor


LISP_LANE = CueLane("LiSP Cues", theme.LISP_LANE)
X32_LANE = CueLane("X32 Snippets", theme.X32_LANE)
LIGHT_CUE_LANE = CueLane("Light Cues", theme.LIGHT_CUE_LANE)

# The lanes from left to right.
LANES = (LISP_LANE, X32_LANE, LIGHT_CUE_LANE)


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


class CueLaneSegments:
    """The cue segments of every lane, in the order of LANES.

    Every cue is labeled by its compact name, a letter and a three digit number:
    L for LiSP cues, S for X32 snippets and Q for light cues. Labels are cut
    to theme.CUE_NAME_LENGTH characters, since nothing more is needed.

    Every new segment of a lane gets the next color of theme.CUE_COLORS, so
    neighbouring cues can always be told apart.
    """

    def __init__(self, script: Script):
        self._row_count = len(script.blocks)
        self._rows_of_blocks = {block.id: row for row, block in enumerate(script.blocks)}
        self._names: tuple[dict[int, list[str]], ...] = tuple({} for _ in LANES)

        for cue in script.lisp_cues:
            self._add(cue.block_id, LISP_LANE, cue.name)
        for snippet in script.x32_snippets:
            self._add(snippet.block_id, X32_LANE, snippet.name)
        for cue in script.light_cues:
            for block_id in cue.block_ids:
                self._add(block_id, LIGHT_CUE_LANE, cue.name)

        self._segments = tuple(self._build_segments(names_by_row) for names_by_row in self._names)

    def of_lane(self, lane: CueLane) -> list[CueSegment]:
        return self._segments[LANES.index(lane)]

    def name_count(self, row: int, lanes: tuple[CueLane, ...]) -> int:
        """The most cue names any of the lanes starts at the row, which the row has to be tall enough for."""
        return max((len(self._names[LANES.index(lane)].get(row, [])) for lane in lanes), default=0)

    def _add(self, block_id: int, lane: CueLane, name: str) -> None:
        row = self._rows_of_blocks.get(block_id)
        if row is not None:
            self._names[LANES.index(lane)].setdefault(row, []).append(name[:theme.CUE_NAME_LENGTH])

    def _build_segments(self, names_by_row: dict[int, list[str]]) -> list[CueSegment]:
        first_rows = sorted(names_by_row)
        segments = []
        for number, first_row in enumerate(first_rows):
            is_last = number + 1 == len(first_rows)
            last_row = self._row_count - 1 if is_last else first_rows[number + 1] - 1
            color = theme.CUE_COLORS[number % len(theme.CUE_COLORS)]
            segments.append(CueSegment(first_row, last_row, tuple(names_by_row[first_row]), color))
        return segments
