from model.block import Block


class LightCueAssigner:
    """Assigns every light effect of the workbook a MagicQ cue number."""

    def assign(self, blocks: list[Block]) -> dict[str, int]:
        return {effect: number for number, effect in enumerate(self.cue_names(blocks), start=1)}

    def cue_names(self, blocks: list[Block]) -> dict[str, str]:
        """Maps every light effect to the name of its cue, in the order the effects first appear in the play."""
        cue_names: dict[str, str] = {}
        for block in blocks:
            if block.light and block.light not in cue_names:
                cue_names[block.light] = block.cue_name()
        return cue_names
