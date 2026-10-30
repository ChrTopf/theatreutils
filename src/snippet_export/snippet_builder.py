from model.actor import Actor
from model.block import Block
from snippet_export.x32_snippet import X32Snippet


class SnippetBuilder:
    """Turns the `mute` / `unmute` annotations of the blocks into X32 snippets.

    Every block that mutes or unmutes at least one actor yields one snippet that
    switches exactly those actors' microphone channels. The channel of an actor
    is looked up in the character roster. Should a channel be muted and unmuted
    by the same block, the unmute wins, so nobody is accidentally silenced.

    Snippets are named after their position in the play, e.g. "2. Akt S3 B415"
    for block 415 in scene 3 of the second act, so the sound engineer can match
    them with the script viewer.
    """

    def build(self, actors: list[Actor], blocks: list[Block]) -> list[X32Snippet]:
        mic_by_actor = {actor.actor: actor.mic for actor in actors}
        return [self._to_snippet(block, mic_by_actor) for block in self._mic_change_blocks(blocks)]

    def snippet_numbers(self, blocks: list[Block]) -> dict[int, int]:
        """Maps the ID of every block yielding a snippet to the snippet's number, as written by SnippetWriter."""
        return {block.id: number for number, block in enumerate(self._mic_change_blocks(blocks))}

    @staticmethod
    def _mic_change_blocks(blocks: list[Block]) -> list[Block]:
        return [block for block in blocks if block.mute or block.unmute]

    def _to_snippet(self, block: Block, mic_by_actor: dict[str, int]) -> X32Snippet:
        snippet = X32Snippet(name=block.cue_name())
        for actor_name in block.mute:
            snippet.set_channel(self._mic(actor_name, block, mic_by_actor), on=False)
        for actor_name in block.unmute:
            snippet.set_channel(self._mic(actor_name, block, mic_by_actor), on=True)
        return snippet

    @staticmethod
    def _mic(actor_name: str, block: Block, mic_by_actor: dict[str, int]) -> int:
        if actor_name not in mic_by_actor:
            raise ValueError(f"Block {block.id}: the actor '{actor_name}' is not listed in the Characters sheet.")
        return mic_by_actor[actor_name]
