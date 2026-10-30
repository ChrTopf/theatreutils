from typing import Optional

from lisp_export.lisp_project import LispProject
from model.block import Block
from model.light_cue_entry import LightCueEntry
from model.lisp_cue_entry import LispCueEntry
from model.script import Script
from model.snippet_entry import SnippetEntry
from snippet_export.x32_snippet import X32Snippet


class ScriptBuilder:
    """Collects the blocks and all cues generated for the decks into the Script read by the script viewer.

    Every cue keeps a reference to the block(s) triggering it, so the viewer
    can show it next to the text it belongs to.
    """

    def build(self, blocks: list[Block], snippets: list[X32Snippet], snippet_numbers: dict[int, int],
              light_cue_numbers: dict[str, int], light_cue_names: dict[str, str],
              lisp_project: Optional[LispProject]) -> Script:
        return Script(
            blocks=blocks,
            lisp_cues=self._lisp_cues(lisp_project),
            x32_snippets=self._snippets(snippets, snippet_numbers),
            light_cues=self._light_cues(blocks, light_cue_numbers, light_cue_names),
        )

    @staticmethod
    def _lisp_cues(lisp_project: Optional[LispProject]) -> list[LispCueEntry]:
        if lisp_project is None:
            return []
        return [LispCueEntry(index=cue["index"], name=cue["name"], description=cue["description"], block_id=block_id)
                for cue, block_id in zip(lisp_project.cues, lisp_project.cue_block_ids)]

    @staticmethod
    def _snippets(snippets: list[X32Snippet], snippet_numbers: dict[int, int]) -> list[SnippetEntry]:
        """Both the snippets and their numbers are in play order, see SnippetBuilder."""
        return [SnippetEntry(number=number + 1, name=snippet.name, block_id=block_id)
                for (block_id, number), snippet in zip(snippet_numbers.items(), snippets)]

    @staticmethod
    def _light_cues(blocks: list[Block], light_cue_numbers: dict[str, int],
                    light_cue_names: dict[str, str]) -> list[LightCueEntry]:
        cues = {effect: LightCueEntry(cue=number, name=light_cue_names[effect], effect=effect)
                for effect, number in light_cue_numbers.items()}
        for block in blocks:
            if block.light in cues:
                cues[block.light].block_ids.append(block.id)
        return sorted(cues.values(), key=lambda cue: cue.cue)
