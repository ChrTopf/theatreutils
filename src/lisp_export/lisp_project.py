from dataclasses import dataclass


@dataclass
class LispProject:
    """A Linux Show Player project and, for every one of its cues, the ID of the block it was generated from.

    `data` is the content of the `.lsp` file. `cue_block_ids` is in the same
    order as its cue list, since LiSP itself has no place to store the block.
    """

    data: dict
    cue_block_ids: list[int]

    @property
    def cues(self) -> list[dict]:
        return self.data["cues"]
