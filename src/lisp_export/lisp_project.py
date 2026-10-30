from dataclasses import dataclass


@dataclass
class LispProject:
    """A Linux Show Player project and, for every one of its cues, the ID of the block it was generated from and its 
    color.
    """

    data: dict
    cue_block_ids: list[int]
    cue_colors: list[str]

    @property
    def cues(self) -> list[dict]:
        return self.data["cues"]
