from textbook_parser.cue import Cue
from textbook_parser.line import Line
from textbook_parser.parser_state import ParserState
from textbook_parser.parsing_context import ParsingContext


class DialogueState(ParserState):
    """Collects the spoken lines following a character cue until a blank line or the next cue."""

    def __init__(self, cue: Cue, cue_line: Line):
        self._cue = cue
        self._cue_line = cue_line
        self._spoken_lines: list[str] = []

    def handle_line(self, context: ParsingContext, line: Line) -> None:
        if context.classifier.match_cue(line.text):
            self._emit_block(context)
            context.return_to_idle(pending_line=line)
        else:
            self._spoken_lines.append(line.text)

    def handle_blank_line(self, context: ParsingContext) -> None:
        self._emit_block(context)
        context.return_to_idle()

    def finish(self, context: ParsingContext) -> None:
        self._emit_block(context)

    def _emit_block(self, context: ParsingContext) -> None:
        context.add_block(
            "dialogue",
            " ".join(self._spoken_lines),
            self._cue_line,
            character=self._cue.character,
            direction=self._cue.direction,
        )
