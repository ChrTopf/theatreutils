from textbook_parser.line import Line
from textbook_parser.parser_state import ParserState
from textbook_parser.parsing_context import ParsingContext


class StageDirectionState(ParserState):
    """Collects a free-form paragraph until a blank line, a structural marker or a cue."""

    def __init__(self, first_line: Line):
        self._first_line = first_line
        self._paragraph_lines = [first_line.text]

    def handle_line(self, context: ParsingContext, line: Line) -> None:
        classifier = context.classifier
        if classifier.is_structural(line.text) or classifier.match_cue(line.text):
            self._emit_block(context)
            context.return_to_idle(pending_line=line)
        else:
            self._paragraph_lines.append(line.text)

    def handle_blank_line(self, context: ParsingContext) -> None:
        self._emit_block(context)
        context.return_to_idle()

    def finish(self, context: ParsingContext) -> None:
        self._emit_block(context)

    def _emit_block(self, context: ParsingContext) -> None:
        paragraph = " ".join(self._paragraph_lines)
        block_type = "command" if context.classifier.is_tech_command(paragraph) else "acting"
        context.add_block(block_type, paragraph, self._first_line)
