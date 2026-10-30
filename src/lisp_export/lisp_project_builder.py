from light_export.magicq_osc import MagicQOsc
from lisp_export.lisp_cue_factory import LispCueFactory
from lisp_export.lisp_project import LispProject
from model.block import Block
from osc_routing.deck_routes import MAGICQ_ROUTE, X32_ROUTE

AUDIO_EXTENSION = ".wav"

# OSC command of the X32 that recalls the snippet in the given slot of the show.
X32_LOAD_PATH = "/load"

# The background colors of the cues in the LiSP cue list, taken by the blocks in turns, so neighbouring blocks differ.
# All share a relative luminance of about 0.16-0.18, so white text on them reaches a contrast of at least 4.5:1 and the
# colors as text on the dark Script Viewer cards at least 3.6:1. They are ordered so that neighbours are far apart in hue.
# Yellow must never be used.
CUE_COLORS = (
    "#2868e8",  # blue
    "#c85000",  # orange
    "#008080",  # teal
    "#d02890",  # magenta
    "#0078b0",  # azure
    "#e02030",  # red
    "#9848e0",  # purple
    "#986a44",  # brown
    "#208838",  # green
)

# Everything around the cue list is taken over from a project saved by LiSP 0.6.5.
PROJECT_META = {
    "plugins": {plugin: "0.6.5" for plugin in (
        "ActionCues", "CacheManager", "CartLayout", "Controller", "GstBackend", "ListLayout", "MediaInfo", "Midi",
        "Network", "Osc", "Presets", "RenameCues", "ReplayGain", "Synchronizer", "Timecode", "Triggers",
    )},
    "version": "0.6.5",
}
PROJECT_SESSION = {
    "layout": {
        "accurate_time": False,
        "auto_continue": True,
        "dbmeters_visible": True,
        "go_key_disabled_while_playing": False,
        "index_column_visible": True,
        "seek_sliders_visible": True,
        "selection_mode": False,
        "view_sizes": [[220, 780], [209, 1273, 418], [1485, 419]],
    },
    "layout_type": "ListLayout",
}


class LispProjectBuilder:
    """Turns the blocks into a Linux Show Player project with one cue per mic change, audio effect and light effect."""

    def __init__(self, cue_factory: LispCueFactory, magicq: MagicQOsc,
                 snippet_numbers: dict[int, int], light_cue_numbers: dict[str, int],
                 include_mutes: bool, include_audio: bool, include_light: bool):
        self.cue_factory = cue_factory
        self.magicq = magicq
        self.snippet_numbers = snippet_numbers
        self.light_cue_numbers = light_cue_numbers
        self.include_mutes = include_mutes
        self.include_audio = include_audio
        self.include_light = include_light

    def build(self, blocks: list[Block]) -> LispProject:
        cues = []
        cue_block_ids = []
        cue_colors = []
        color_number = 0
        for block in blocks:
            block_cues = self._block_cues(block)
            if not block_cues:
                continue
            color = CUE_COLORS[color_number % len(CUE_COLORS)]
            color_number += 1
            for cue in block_cues:
                self.cue_factory.set_color(cue, color)
            cues += block_cues
            cue_block_ids += [block.id] * len(block_cues)
            cue_colors += [color] * len(block_cues)
        for index, cue in enumerate(cues):
            cue["index"] = index
        return LispProject({"cues": cues, "meta": PROJECT_META, "session": PROJECT_SESSION}, cue_block_ids, cue_colors)

    def _block_cues(self, block: Block) -> list[dict]:
        cues = []
        if self.include_mutes and block.id in self.snippet_numbers:
            cues.append(self._mute_cue(block))
        if self.include_audio and block.audio_effect:
            cues.append(self._audio_cue(block))
        if self.include_light and block.light:
            cues.append(self._light_cue(block))

        for cue in cues:
            cue["name"] = block.cue_name()
        for cue in cues[:-1]:
            cue["next_action"] = "TriggerAfterWait"
        return cues

    def _mute_cue(self, block: Block) -> dict:
        lines = []
        if block.mute:
            lines.append(f"Mute {', '.join(block.mute)}")
        if block.unmute:
            lines.append(f"Unmute {', '.join(block.unmute)}")
        snippet_slot = self.snippet_numbers[block.id]
        return self.cue_factory.osc_cue(
            name="",
            description=",\n".join(lines),
            path=f"/{X32_ROUTE}{X32_LOAD_PATH}",
            args=[
                self.cue_factory.osc_string_arg("snippet"), 
                self.cue_factory.osc_integer_arg(snippet_slot),
                self.cue_factory.osc_integer_arg(0),
                self.cue_factory.osc_integer_arg(0)
            ],
        )

    def _audio_cue(self, block: Block) -> dict:
        file_name = block.audio_effect
        if not file_name.lower().endswith(AUDIO_EXTENSION):
            file_name += AUDIO_EXTENSION
        return self.cue_factory.media_cue(name="", description=f"Play {file_name}", uri=file_name)

    def _light_cue(self, block: Block) -> dict:
        cue_number = self.light_cue_numbers[block.light]
        return self.cue_factory.osc_cue(
            name="",
            description=f"{block.light} (MagicQ cue {cue_number})",
            path=f"/{MAGICQ_ROUTE}{self.magicq.jump_to_cue_path(cue_number)}",
            args=[],
        )
