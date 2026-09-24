import re

from actor import Actor
from block import Block
from page import Page

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


class TextbookParser:
    """Parses raw textbook text into a sequence of Block objects."""

    def __init__(self, actors: list[Actor]):
        self._known_names = Actor.known_character_names(actors)

    def parse(self, pages: list[Page]) -> list[Block]:
        lines, line_page_numbers = self._split_into_lines(pages)
        total_lines = len(lines)
        index = 0
        next_id = 0
        current_part = "Vorspann"
        current_scene = 1
        awaiting_cast_list = False
        blocks: list[Block] = []

        def make_block(block_type: str, block_text: str, start_index: int, character: str = None, direction: str = None) -> Block:
            nonlocal next_id
            block = Block(
                id=next_id,
                type=block_type,
                part=current_part,
                scene=current_scene,
                page=line_page_numbers[start_index],
                text=block_text,
                character=character,
                direction=direction,
            )
            next_id += 1
            return block

        def match_known_cue(candidate: str):
            match = CUE_REGEX.match(candidate)
            if match and match.group(1).strip() in self._known_names:
                return match
            return None

        while index < total_lines:
            line = lines[index].strip()
            if not line:
                index += 1
                continue
            start_index = index

            if OPENING_REGEX.match(line):
                current_part = line
                awaiting_cast_list = False
                index += 1
                continue

            if ACT_REGEX.match(line):
                current_part = line
                awaiting_cast_list = False
                index += 1
                continue

            scene_match = SCENE_REGEX.match(line)
            if scene_match:
                current_scene = int(scene_match.group(1))
                awaiting_cast_list = True
                index += 1
                continue

            if CURTAIN_REGEX.match(line):
                blocks.append(make_block("command", line, start_index))
                awaiting_cast_list = False
                index += 1
                continue

            cue_match = match_known_cue(line)
            if cue_match:
                character = cue_match.group(1).strip()
                direction = cue_match.group(2)
                awaiting_cast_list = False
                index += 1
                spoken_lines = []
                while index < total_lines and lines[index].strip() and not match_known_cue(lines[index].strip()):
                    spoken_lines.append(lines[index].strip())
                    index += 1
                blocks.append(make_block("dialogue", " ".join(spoken_lines), start_index, character=character, direction=direction))
                continue

            # A bare comma-separated line right after a scene heading lists the
            # characters present in that scene.
            if awaiting_cast_list:
                names = [name.strip() for name in line.split(",") if name.strip()]
                awaiting_cast_list = False
                if names and all(name in self._known_names for name in names):
                    blocks.append(make_block("acting", line, start_index))
                    index += 1
                    continue

            # Free-form stage-direction paragraph: gather lines until the next
            # blank line or the next structural marker/cue.
            paragraph_lines = [line]
            index += 1
            while index < total_lines and lines[index].strip():
                candidate = lines[index].strip()
                if (OPENING_REGEX.match(candidate) or CURTAIN_REGEX.match(candidate)
                        or ACT_REGEX.match(candidate) or SCENE_REGEX.match(candidate)
                        or match_known_cue(candidate)):
                    break
                paragraph_lines.append(candidate)
                index += 1
            paragraph = " ".join(paragraph_lines)
            block_type = "command" if self._is_tech_command(paragraph) else "acting"
            blocks.append(make_block(block_type, paragraph, start_index))

        return blocks

    @staticmethod
    def _is_tech_command(paragraph: str) -> bool:
        lowered = paragraph.lower()
        return any(re.search(rf"\b{keyword}\b", lowered) for keyword in TECH_KEYWORDS)

    @staticmethod
    def _split_into_lines(pages: list[Page]) -> tuple[list[str], list[int]]:
        """Flattens the pages into one list of lines, plus the page number each line came from.

        Pages are concatenated without a separator so that dialogue and paragraphs
        spanning a page break are still recognized as a single block.
        """
        lines: list[str] = []
        line_page_numbers: list[int] = []
        for page in pages:
            page_lines = page.text.splitlines()
            lines.extend(page_lines)
            line_page_numbers.extend([page.number] * len(page_lines))
        return lines, line_page_numbers
