from PyQt5.QtGui import QColor

from model.block import Block
from model.script import Script
from script_viewer_ui import theme
from script_viewer_ui.cue_lane import CueLane
from script_viewer_ui.cue_segment import CueSegment
from script_viewer_ui.viewer_settings import ViewerSettings

LISP_LANE = CueLane("LiSP Cues", "L", theme.LISP_LANE)
X32_LANE = CueLane("X32 Snippets", "S", theme.X32_LANE)
LIGHT_CUE_LANE = CueLane("Light Cues", "Q", theme.LIGHT_CUE_LANE)

# The lanes from left to right.
LANES = (LISP_LANE, X32_LANE, LIGHT_CUE_LANE)

# Separates the names of several cues of one deck triggered by the same block.
CUE_NAME_SEPARATOR = ", "

# The segments of a lane are numbered from this number on.
FIRST_SEGMENT_NUMBER = 1
# Replaces the letter of the lane in front of the segment numbers, unless the settings ask for the letters.
NUMBER_PREFIX = "#"

UNMUTE_PREFIX = "▲ "
MUTE_PREFIX = "▼ "
AUDIO_PREFIX = "♪ "
LIGHT_PREFIX = "☀ "

class CueLaneSegments:
    """The cue segments of every lane, in the order of LANES."""

    def __init__(self, script: Script, settings: ViewerSettings):
        self._blocks = script.blocks
        self._row_count = len(script.blocks)
        self._rows_of_blocks = {block.id: row for row, block in enumerate(script.blocks)}
        self._names: tuple[dict[int, list[str]], ...] = tuple({} for _ in LANES)
        self._colors: tuple[dict[int, QColor], ...] = tuple({} for _ in LANES)

        for cue in script.lisp_cues:
            self._add(cue.block_id, LISP_LANE, cue.name, QColor(cue.color))
        for snippet in script.x32_snippets:
            self._add(snippet.block_id, X32_LANE, snippet.name, X32_LANE.color)
        for cue in script.light_cues:
            for block_id in cue.block_ids:
                self._add(block_id, LIGHT_CUE_LANE, cue.name, LIGHT_CUE_LANE.color)

        self.apply_settings(settings)

    def apply_settings(self, settings: ViewerSettings) -> None:
        self._settings = settings
        self._segments = tuple(self._build_segments(lane) for lane in LANES)
        self._segments_by_first_row = tuple({segment.first_row: segment for segment in segments}
                                            for segments in self._segments)

    def of_lane(self, lane: CueLane) -> list[CueSegment]:
        return self._segments[LANES.index(lane)]

    def next_segment(self, lane: CueLane, row: int) -> CueSegment | None:
        return next((segment for segment in self.of_lane(lane) if segment.first_row > row), None)

    def starting_at(self, row: int, lanes: tuple[CueLane, ...]) -> list[CueSegment]:
        segments = (self._segments_by_first_row[LANES.index(lane)].get(row) for lane in lanes)
        return [segment for segment in segments if segment is not None]

    def _add(self, block_id: int, lane: CueLane, name: str, color: QColor) -> None:
        row = self._rows_of_blocks.get(block_id)
        if row is not None:
            self._names[LANES.index(lane)].setdefault(row, []).append(name)
            self._colors[LANES.index(lane)].setdefault(row, color)

    def _build_segments(self, lane: CueLane) -> list[CueSegment]:
        names_by_row = self._names[LANES.index(lane)]
        colors_by_row = self._colors[LANES.index(lane)]
        first_rows = sorted(names_by_row)
        prefix = lane.prefix if self._settings.lane_letter_prefixes else NUMBER_PREFIX
        segments = []
        for index, first_row in enumerate(first_rows):
            is_last = index + 1 == len(first_rows)
            last_row = self._row_count - 1 if is_last else first_rows[index + 1] - 1
            label = f"{prefix}{index + FIRST_SEGMENT_NUMBER}"
            name = CUE_NAME_SEPARATOR.join(dict.fromkeys(names_by_row[first_row]))
            details = self._details(lane, self._blocks[first_row])
            segments.append(CueSegment(first_row, last_row, label, name, colors_by_row[first_row], details))
        return segments

    def _details(self, lane: CueLane, block: Block) -> tuple[str, ...]:
        if lane is LISP_LANE:
            details = self._mic_details(block) if self._settings.mutes_in_lisp_lane else []
            if block.audio_effect:
                details.append(AUDIO_PREFIX + block.audio_effect)
            return tuple(details)
        if lane is X32_LANE:
            return tuple(self._mic_details(block))
        if lane is LIGHT_CUE_LANE and block.light:
            return (LIGHT_PREFIX + block.light,)
        return ()

    @staticmethod
    def _mic_details(block: Block) -> list[str]:
        unmutes = [UNMUTE_PREFIX + actor for actor in block.unmute]
        mutes = [MUTE_PREFIX + actor for actor in block.mute]
        return unmutes + mutes
