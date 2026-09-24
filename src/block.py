from dataclasses import dataclass
from typing import Optional


@dataclass
class Block:
    """A single unit of the textbook: spoken dialogue, a stage direction, or a tech cue.

    Deliberately excludes actor/mic/characters-present information - those are
    correlated against the character roster in a later step, not stored here.
    """

    id: int
    type: str
    part: str
    scene: int
    text: str
    character: Optional[str] = None
    direction: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "part": self.part,
            "scene": self.scene,
            "text": self.text,
            "character": self.character,
            "direction": self.direction,
        }
