from textbook_parser.cast_list_state import CastListState
from textbook_parser.dialogue_state import DialogueState
from textbook_parser.line import Line
from textbook_parser.parser_state import ParserState
from textbook_parser.parsing_context import ParsingContext
from textbook_parser.stage_direction_state import StageDirectionState


class IdleState(ParserState):
    """Between two blocks: decides what the next line starts."""

    def handle_line(self, context: ParsingContext, line: Line) -> None:
        classifier = context.classifier
        scene_number = classifier.scene_number(line.text)
        cue = classifier.match_cue(line.text)

        if classifier.is_part_heading(line.text):
            context.start_part(line.text)
        elif scene_number is not None:
            context.start_scene(scene_number)
            context.transition_to(CastListState())
        elif classifier.is_curtain(line.text):
            context.add_block("command", line.text, line)
        elif cue is not None:
            context.transition_to(DialogueState(cue, line))
        else:
            context.transition_to(StageDirectionState(line))
