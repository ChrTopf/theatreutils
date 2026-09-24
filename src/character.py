from dataclasses import dataclass


@dataclass
class Character:
    """A role played by an actor, as defined in characters.json."""

    name: str
    actions: int

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        return cls(name=data["name"], actions=data["actions"])

    def to_dict(self) -> dict:
        return {"name": self.name, "actions": self.actions}
