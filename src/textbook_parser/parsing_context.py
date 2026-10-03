from typing import TYPE_CHECKING, Optional

from model.block import Block
from textbook_parser.line import Line
from textbook_parser.line_classifier import LineClassifier

if TYPE_CHECKING:
    from textbook_parser.parser_state import ParserState


class ParsingContext:
    """The context of the parser state machine.

    Holds everything that outlives a single state: the current position in the
    play (part and scene), the blocks produced so far and the active state,
    to which every incoming line is delegated. The machine starts in the idle
    state, which every other state returns to once its block is complete.
    """

    def __init__(self, classifier: LineClassifier, idle_state: "ParserState"):
        self.classifier = classifier
        self.current_part = "Vorspann"
        self.current_scene = 1
        self.blocks: list[Block] = []
        self._idle_state = idle_state
        self._state = idle_state

    def transition_to(self, state: "ParserState") -> None:
        self._state = state

    def return_to_idle(self, pending_line: Optional[Line] = None) -> None:
        """Switches back to the idle state and lets it process `pending_line`, if given."""
        self._state = self._idle_state
        if pending_line is not None:
            self.handle_line(pending_line)

    def handle_line(self, line: Line) -> None:
        if line.is_blank:
            self._state.handle_blank_line(self)
        else:
            self._state.handle_line(self, line)

    def finish(self) -> None:
        self._state.finish(self)

    def start_part(self, part: str) -> None:
        self.current_part = part

    def start_scene(self, scene: int) -> None:
        self.current_scene = scene

    def add_block(self, block_type: str, text: str, start_line: Line,
                  character: Optional[str] = None, direction: Optional[str] = None) -> None:
        self.blocks.append(Block(
            id=len(self.blocks),
            type=block_type,
            part=self.current_part,
            scene=self.current_scene,
            page=start_line.page_number,
            text=text,
            character=character,
            direction=direction,
        ))
