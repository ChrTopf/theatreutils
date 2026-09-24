from typing import Optional

from actor import Actor
from block import Block


class MicAnnotator:
    """Fills the `mute` / `unmute` columns of the blocks, i.e. when which actor's mic is switched.

    Every actor starts muted. An actor is unmuted `unmute_padding` blocks before
    they speak up. After speaking, they are muted again when
      - they do not speak for the next `threshold_turns` blocks (muted right after their line), or
      - a scene starts in which they do not speak (muted at the start of that scene).
    A mute is dropped if the actor would have to be unmuted again at or before
    that very block anyway, so a mic is never switched off and on at once.
    """

    def __init__(self, threshold_turns: int, unmute_padding: int):
        self._threshold_turns = threshold_turns
        self._unmute_padding = unmute_padding

    def annotate(self, actors: list[Actor], blocks: list[Block]) -> None:
        scene_starts = self._scene_start_indices(blocks)
        for actor in actors:
            speaking_indices = self._speaking_indices(actor, blocks)
            if speaking_indices:
                self._annotate_actor(actor.actor, speaking_indices, scene_starts, blocks)

    def _annotate_actor(self, actor_name: str, speaking_indices: list[int],
                        scene_starts: list[int], blocks: list[Block]) -> None:
        first_unmute = max(speaking_indices[0] - self._unmute_padding, 0)
        blocks[first_unmute].unmute.append(actor_name)

        # The end of the play counts as a line spoken far in the future, so the
        # actor gets muted after their last line by the very same rules.
        end_of_play = len(blocks) + self._threshold_turns + self._unmute_padding
        next_speaking_indices = speaking_indices[1:] + [end_of_play]

        for spoken, next_spoken in zip(speaking_indices, next_speaking_indices):
            mute_index = self._mute_index(spoken, next_spoken, scene_starts, blocks)
            unmute_index = next_spoken - self._unmute_padding
            if mute_index is None or mute_index >= min(unmute_index, len(blocks)):
                continue
            blocks[mute_index].mute.append(actor_name)
            if next_spoken < len(blocks):
                blocks[unmute_index].unmute.append(actor_name)

    def _mute_index(self, spoken: int, next_spoken: int,
                    scene_starts: list[int], blocks: list[Block]) -> Optional[int]:
        """The block at which the actor is muted between two of their lines, or None if they stay unmuted."""
        silent_blocks = next_spoken - spoken - 1
        if silent_blocks >= self._threshold_turns:
            return spoken + 1
        next_scene = self._scene_key(blocks[next_spoken]) if next_spoken < len(blocks) else None
        for scene_start in scene_starts:
            if spoken < scene_start < next_spoken and self._scene_key(blocks[scene_start]) != next_scene:
                return scene_start
        return None

    @staticmethod
    def _speaking_indices(actor: Actor, blocks: list[Block]) -> list[int]:
        character_names = {character.name for character in actor.characters}
        return [index for index, block in enumerate(blocks)
                if block.type == "dialogue" and block.character in character_names]

    @classmethod
    def _scene_start_indices(cls, blocks: list[Block]) -> list[int]:
        return [index for index, block in enumerate(blocks)
                if index == 0 or cls._scene_key(block) != cls._scene_key(blocks[index - 1])]

    @staticmethod
    def _scene_key(block: Block) -> tuple[str, int]:
        return block.part, block.scene
