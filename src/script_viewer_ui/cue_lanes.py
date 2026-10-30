from model.script import Script
from script_viewer_ui import theme
from script_viewer_ui.cue_lane import CueLane
from script_viewer_ui.cue_segment import CueSegment

LISP_LANE = CueLane("LiSP Cues", theme.LISP_LANE)
X32_LANE = CueLane("X32 Snippets", theme.X32_LANE)
LIGHT_CUE_LANE = CueLane("Light Cues", theme.LIGHT_CUE_LANE)

# The lanes from left to right.
LANES = (LISP_LANE, X32_LANE, LIGHT_CUE_LANE)

class CueLaneSegments:
    """The cue segments of every lane, in the order of LANES."""

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

    def next_segment(self, lane: CueLane, row: int) -> CueSegment | None:
        return next((segment for segment in self.of_lane(lane) if segment.first_row > row), None)

    def name_count(self, row: int, lanes: tuple[CueLane, ...]) -> int:
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
