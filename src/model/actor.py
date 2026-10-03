from dataclasses import dataclass, field
import json

from model.character import Character


@dataclass
class Actor:
    """A performer (microphone) and the characters they play, as defined in characters.json."""

    mic: int
    actor: str
    characters: list[Character] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Actor":
        return cls(
            mic=data["mic"],
            actor=data["actor"],
            characters=[Character.from_dict(character) for character in data["characters"]],
        )

    def to_dict(self) -> dict:
        return {
            "mic": self.mic,
            "actor": self.actor,
            "characters": [character.to_dict() for character in self.characters],
        }

    @classmethod
    def load_list(cls, path: str) -> list["Actor"]:
        with open(path, "r", encoding="utf-8") as characters_file:
            raw = json.load(characters_file)
        return [cls.from_dict(entry) for entry in raw]

    @staticmethod
    def known_character_names(actors: list["Actor"]) -> set[str]:
        return {character.name for actor in actors for character in actor.characters}
