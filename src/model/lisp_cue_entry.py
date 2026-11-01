from dataclasses import dataclass


@dataclass
class LispCueEntry:
    """A cue of the generated Linux Show Player project"""

    number: int
    name: str
    description: str
    color: str
    block_id: int

    @classmethod
    def from_dict(cls, data: dict) -> "LispCueEntry":
        return cls(number=data["number"], name=data["name"], description=data["description"], color=data["color"],
                   block_id=data["block_id"])

    def to_dict(self) -> dict:
        return {"number": self.number, "name": self.name, "description": self.description, "color": self.color,
                "block_id": self.block_id}
