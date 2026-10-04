from dataclasses import dataclass


@dataclass
class SnippetEntry:
    """A generated X32 snippet, identified by its number on the console, and the block recalling it."""

    number: int
    name: str
    block_id: int

    @classmethod
    def from_dict(cls, data: dict) -> "SnippetEntry":
        return cls(number=data["number"], name=data["name"], block_id=data["block_id"])

    def to_dict(self) -> dict:
        return {"number": self.number, "name": self.name, "block_id": self.block_id}
