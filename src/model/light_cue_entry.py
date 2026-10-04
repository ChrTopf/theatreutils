from dataclasses import dataclass, field


@dataclass
class LightCueEntry:
    """A light cue to be programmed into the MagicQ and the blocks triggering it."""

    cue: int
    name: str
    block_ids: list[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "LightCueEntry":
        return cls(cue=data["cue"], name=data["name"], block_ids=list(data["block_ids"]))

    def to_dict(self) -> dict:
        return {"cue": self.cue, "name": self.name, "block_ids": self.block_ids}
