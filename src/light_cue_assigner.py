from block import Block


class LightCueAssigner:
    """Assigns every light effect of the workbook a MagicQ cue number.

    Each effect name gets one cue, numbered from 1 in the order the effects
    first appear in the play. An effect used by several blocks reuses its cue,
    so it only has to be programmed once on the desk.
    """

    def assign(self, blocks: list[Block]) -> dict[str, int]:
        cue_numbers: dict[str, int] = {}
        for block in blocks:
            if block.light and block.light not in cue_numbers:
                cue_numbers[block.light] = len(cue_numbers) + 1
        return cue_numbers
