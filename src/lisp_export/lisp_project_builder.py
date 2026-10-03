from model.block import Block
from lisp_export.lisp_cue_factory import LispCueFactory
from light_export.magicq_osc import MagicQOsc
from osc_routing.deck_routes import MAGICQ_ROUTE, X32_ROUTE

AUDIO_EXTENSION = ".wav"

# OSC command of the X32 that recalls the snippet with the given number.
X32_SNIPPET_RECALL_PATH = "/-action/gosnippet"

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
    """Turns the blocks into a Linux Show Player project with one cue per mic change, audio effect and light effect.

    - Mic changes recall the X32 snippet generated for the block via OSC.
    - Audio effects play `<Audio Effect>.wav`, located next to the project file.
    - Light effects make the MagicQ jump to the pre-programmed cue of the effect via OSC.

    LiSP sends all OSC messages to a single host, the OSC relay (osc_relay.py).
    The first address segment tells the relay which deck the message is for,
    e.g. `/x32/-action/gosnippet` or `/mq/pb/1/5`, and is removed by it.

    A block with a single action becomes a single cue. A block with several
    actions becomes a collection cue that starts them at the same time, followed
    by the actions themselves, whose names are prefixed with "--".
    """

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

    def build(self, blocks: list[Block]) -> dict:
        cues = []
        for block in blocks:
            cues += self._block_cues(block)
        for index, cue in enumerate(cues):
            cue["index"] = index
        return {"cues": cues, "meta": PROJECT_META, "session": PROJECT_SESSION}

    def _block_cues(self, block: Block) -> list[dict]:
        block_name = f"{block.part} Scene {block.scene} Block {block.id}"
        actions = self._action_cues(block, block_name)
        if len(actions) <= 1:
            return actions
        collection = self.cue_factory.collection_cue(block_name, "Executes multiple actions at once", actions)
        return [collection] + actions

    def _action_cues(self, block: Block, block_name: str) -> list[dict]:
        """The cues of the block's actions. Named after the block as long as they are its only action."""
        cues = []
        if self.include_mutes and block.id in self.snippet_numbers:
            cues.append(("Mutes", self._mute_cue(block)))
        if self.include_audio and block.audio_effect:
            cues.append(("Sound", self._audio_cue(block)))
        if self.include_light and block.light:
            cues.append(("Light", self._light_cue(block)))

        if len(cues) == 1:
            cues[0][1]["name"] = block_name
        else:
            for suffix, cue in cues:
                cue["name"] = f"-- {block_name} {suffix}"
        return [cue for _, cue in cues]

    def _mute_cue(self, block: Block) -> dict:
        lines = []
        if block.mute:
            lines.append(f"Mute {', '.join(block.mute)}")
        if block.unmute:
            lines.append(f"Unmute {', '.join(block.unmute)}")
        snippet_number = self.snippet_numbers[block.id]
        return self.cue_factory.osc_cue(
            name="",
            description=",\n".join(lines),
            path=f"/{X32_ROUTE}{X32_SNIPPET_RECALL_PATH}",
            args=[self.cue_factory.osc_integer_arg(snippet_number)],
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
