from dataclasses import dataclass

from PyQt5.QtGui import QColor

from model.script import Script
from script_viewer_ui import theme


@dataclass(frozen=True, eq=False)
class CueLane:
    """A colored column running down the page next to the block cards, listing the cues of one deck."""

    name: str
    color: QColor
    dimmed_color: QColor


LISP_LANE = CueLane("LiSP Cues", theme.LISP_LANE, theme.DIMMED_LISP_LANE)
X32_LANE = CueLane("X32 Snippets", theme.X32_LANE, theme.DIMMED_X32_LANE)
LIGHT_CUE_LANE = CueLane("Light Cues", theme.LIGHT_CUE_LANE, theme.DIMMED_LIGHT_CUE_LANE)

# The lanes from left to right.
LANES = (LISP_LANE, X32_LANE, LIGHT_CUE_LANE)


class CueLaneLines:
    """The lines every block shows in the cue lanes, one list of lines per lane in the order of LANES.

    - LiSP cues: the index in the LiSP cue list and the name of the cue.
    - X32 snippets: the snippet number on the console and its name.
    - Light cues: the MagicQ cue number and the name of the light effect.
    """

    def __init__(self, script: Script):
        self._lines: dict[int, tuple[list[str], ...]] = {}
        for cue in script.lisp_cues:
            self._add(cue.block_id, LISP_LANE, f"{cue.index}  {cue.name}")
        for snippet in script.x32_snippets:
            self._add(snippet.block_id, X32_LANE, f"#{snippet.number}  {snippet.name}")
        for cue in script.light_cues:
            for block_id in cue.block_ids:
                self._add(block_id, LIGHT_CUE_LANE, f"Q{cue.cue}  {cue.name}")

    def of_block(self, block_id: int) -> tuple[list[str], ...]:
        return self._lines.get(block_id, tuple([] for _ in LANES))

    def _add(self, block_id: int, lane: CueLane, line: str) -> None:
        lines = self._lines.setdefault(block_id, tuple([] for _ in LANES))
        lines[LANES.index(lane)].append(line)
