from dataclasses import dataclass, field
import json

from model.block import Block
from model.light_cue_entry import LightCueEntry
from model.lisp_cue_entry import LispCueEntry
from model.snippet_entry import SnippetEntry

FORMAT_VERSION = 3


@dataclass
class Script:
    """The script as exported by the cue generator for the script viewer.

    Holds the blocks of the workbook together with the cues generated for the
    decks, each of which refers back to the block(s) triggering it.
    """

    blocks: list[Block] = field(default_factory=list)
    lisp_cues: list[LispCueEntry] = field(default_factory=list)
    x32_snippets: list[SnippetEntry] = field(default_factory=list)
    light_cues: list[LightCueEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Script":
        version = data.get("version")
        if version != FORMAT_VERSION:
            raise ValueError(f"Unsupported script format version {version}, expected {FORMAT_VERSION}.")
        return cls(
            blocks=[Block.from_dict(block) for block in data["blocks"]],
            lisp_cues=[LispCueEntry.from_dict(cue) for cue in data["lisp_cues"]],
            x32_snippets=[SnippetEntry.from_dict(snippet) for snippet in data["x32_snippets"]],
            light_cues=[LightCueEntry.from_dict(cue) for cue in data["light_cues"]],
        )

    def to_dict(self) -> dict:
        return {
            "version": FORMAT_VERSION,
            "blocks": [block.to_dict() for block in self.blocks],
            "lisp_cues": [cue.to_dict() for cue in self.lisp_cues],
            "x32_snippets": [snippet.to_dict() for snippet in self.x32_snippets],
            "light_cues": [cue.to_dict() for cue in self.light_cues],
        }

    @classmethod
    def load(cls, path: str) -> "Script":
        with open(path, "r", encoding="utf-8") as script_file:
            return cls.from_dict(json.load(script_file))
