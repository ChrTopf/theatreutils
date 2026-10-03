from typing import Optional

from model.block import Block


class SceneIndex:
    """Where every scene of every part of the show begins.

    Parts and scenes are reported in the order in which they appear in the
    script. If the same part and scene number appears again later in the script,
    only its first block is remembered, because that is where one wants to jump.
    """

    def __init__(self, blocks: list[Block]):
        self._first_row: dict[tuple[str, int], int] = {}
        self._scenes_by_part: dict[str, list[int]] = {}
        for row, block in enumerate(blocks):
            key = (block.part, block.scene)
            if key in self._first_row:
                continue
            self._first_row[key] = row
            self._scenes_by_part.setdefault(block.part, []).append(block.scene)

    def parts(self) -> list[str]:
        return list(self._scenes_by_part)

    def scenes(self, part: str) -> list[int]:
        return self._scenes_by_part.get(part, [])

    def first_row_of(self, part: str, scene: int) -> Optional[int]:
        return self._first_row.get((part, scene))
