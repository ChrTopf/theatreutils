import csv
import os

from model.actor import Actor
from model.block import Block

HEADERS = ("Mic", "Actor")
# Marks the parts an actor plays in.
PLAYING = "x"


class CastListWriter:
    """Writes the list of actors and the parts of the play they play in as a CSV file.

    Every row names the microphone and the actor, followed by one column per
    part in the order of the play, marked if one of the actor's characters
    has a block in that part. The rows keep the order of the Characters sheet,
    so actors without any block in the play are listed with no part marked.
    """

    def write(self, actors: list[Actor], blocks: list[Block], output_path: str) -> None:
        parts = list(dict.fromkeys(block.part for block in blocks))

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(HEADERS + tuple(parts))
            for actor in actors:
                played_parts = self._played_parts(actor, blocks)
                writer.writerow((actor.mic, actor.actor) + tuple(PLAYING if part in played_parts else "" for part in parts))

    @staticmethod
    def _played_parts(actor: Actor, blocks: list[Block]) -> set[str]:
        character_names = {character.name for character in actor.characters}
        return {block.part for block in blocks if block.character in character_names}
