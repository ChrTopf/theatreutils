from textbook_parser.line import Line
from textbook_parser.parser_state import ParserState
from textbook_parser.parsing_context import ParsingContext


class CastListState(ParserState):
    """Right after a scene heading, where a line may list the characters present in that scene."""

    def handle_line(self, context: ParsingContext, line: Line) -> None:
        if context.classifier.is_cast_list(line.text):
            context.add_block("acting", line.text, line)
            context.return_to_idle()
        else:
            context.return_to_idle(pending_line=line)
