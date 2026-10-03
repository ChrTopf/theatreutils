import csv
import os

from model.block import Block

HEADERS = ("Cue", "Effect", "Blocks")


class LightCueListWriter:
    """Writes the list of light cues that must be programmed into the MagicQ as a CSV file.

    Every row names the cue number, the effect and the IDs of the blocks
    triggering it, so the light designer knows where in the play it is used.
    """

    def write(self, cue_numbers: dict[str, int], blocks: list[Block], output_path: str) -> None:
        block_ids: dict[str, list[str]] = {effect: [] for effect in cue_numbers}
        for block in blocks:
            if block.light in block_ids:
                block_ids[block.light].append(str(block.id))

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(HEADERS)
            for effect, cue_number in sorted(cue_numbers.items(), key=lambda item: item[1]):
                writer.writerow((cue_number, effect, ", ".join(block_ids[effect])))
