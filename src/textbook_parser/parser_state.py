from abc import ABC, abstractmethod

from textbook_parser.line import Line
from textbook_parser.parsing_context import ParsingContext


class ParserState(ABC):
    """A state of the parser state machine (State pattern).

    Each state decides how to react to the next line and which state follows.
    Blank lines and the end of the input are ignored unless a state overrides
    the corresponding hook.
    """

    @abstractmethod
    def handle_line(self, context: ParsingContext, line: Line) -> None:
        ...

    def handle_blank_line(self, context: ParsingContext) -> None:
        pass

    def finish(self, context: ParsingContext) -> None:
        pass
