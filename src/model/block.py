from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Block:
    """A single unit of the textbook: spoken dialogue, a stage direction, or a tech cue.

    Deliberately excludes actor/mic/characters-present information - those are
    correlated against the character roster in a later step, not stored here.
    The only exception are the `mute` / `unmute` actor names, which that later
    step (see MicAnnotator) writes back onto the block.
    """

    id: int
    type: str
    part: str
    scene: int
    page: int
    text: str
    character: Optional[str] = None
    direction: Optional[str] = None
    mute: list[str] = field(default_factory=list)
    unmute: list[str] = field(default_factory=list)
    audio_effect: Optional[str] = None
    light: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        return cls(
            id=data["id"],
            type=data["type"],
            part=data["part"],
            scene=data["scene"],
            page=data["page"],
            text=data["text"],
            character=data.get("character"),
            direction=data.get("direction"),
            mute=list(data.get("mute", [])),
            unmute=list(data.get("unmute", [])),
            audio_effect=data.get("audio_effect"),
            light=data.get("light"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "part": self.part,
            "scene": self.scene,
            "page": self.page,
            "text": self.text,
            "character": self.character,
            "direction": self.direction,
            "mute": self.mute,
            "unmute": self.unmute,
            "audio_effect": self.audio_effect,
            "light": self.light,
        }
