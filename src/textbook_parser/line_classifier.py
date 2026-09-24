import re
from typing import Optional

from textbook_parser.cue import Cue

OPENING_REGEX = re.compile(r"^Vorspann$")
CURTAIN_REGEX = re.compile(r"^Vorhang$")
ACT_REGEX = re.compile(r"^\d+\.\s*Akt$")
SCENE_REGEX = re.compile(r"^(\d+)\.\s*Szene$")
CUE_REGEX = re.compile(r"^([^:]+):\s*(?:\((.*?)\))?\s*$")

# Heuristic keywords that mark a stage-direction paragraph as a tech
# instruction (light/sound/etc.) rather than a description of what an
# actor is doing. Textbooks that mark tech cues differently should extend
# this list.
TECH_KEYWORDS = (
    "licht", "beleuchtung", "spot", "verdunkelung", "blackout",
    "ton", "musik", "sound", "geräusch", "einspieler", "nebel",
)


class LineClassifier:
    """Recognizes what kind of textbook element a single (non-blank) line represents."""

    def __init__(self, known_character_names: set[str]):
        self._known_character_names = known_character_names

    @staticmethod
    def is_part_heading(text: str) -> bool:
        return bool(OPENING_REGEX.match(text) or ACT_REGEX.match(text))

    @staticmethod
    def scene_number(text: str) -> Optional[int]:
        match = SCENE_REGEX.match(text)
        return int(match.group(1)) if match else None

    @staticmethod
    def is_curtain(text: str) -> bool:
        return bool(CURTAIN_REGEX.match(text))

    def is_structural(self, text: str) -> bool:
        return self.is_part_heading(text) or self.scene_number(text) is not None or self.is_curtain(text)

    def match_cue(self, text: str) -> Optional[Cue]:
        match = CUE_REGEX.match(text)
        if not match:
            return None
        character = match.group(1).strip()
        if character not in self._known_character_names:
            return None
        return Cue(character=character, direction=match.group(2))

    def is_cast_list(self, text: str) -> bool:
        """A comma-separated line consisting only of known character names."""
        names = [name.strip() for name in text.split(",") if name.strip()]
        return bool(names) and all(name in self._known_character_names for name in names)

    @staticmethod
    def is_tech_command(text: str) -> bool:
        lowered = text.lower()
        return any(re.search(rf"\b{keyword}\b", lowered) for keyword in TECH_KEYWORDS)
