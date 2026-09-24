from actor import Actor
from block import Block
from page import Page
from textbook_parser.idle_state import IdleState
from textbook_parser.line import lines_from_pages
from textbook_parser.line_classifier import LineClassifier
from textbook_parser.parsing_context import ParsingContext


class TextbookParser:
    """Parses the pages of a textbook into a sequence of Block objects.

    The parsing itself is a line-driven state machine: every line is handed to
    a ParsingContext, which delegates it to its currently active ParserState.
    """

    def __init__(self, actors: list[Actor]):
        self._classifier = LineClassifier(Actor.known_character_names(actors))

    def parse(self, pages: list[Page]) -> list[Block]:
        context = ParsingContext(self._classifier, idle_state=IdleState())
        for line in lines_from_pages(pages):
            context.handle_line(line)
        context.finish()
        return context.blocks
