# Only the first 10 playbacks can be controlled with MagicQ's built-in OSC addresses.
FIRST_PLAYBACK = 1
LAST_PLAYBACK = 10


class MagicQOsc:
    """Builds the built-in OSC addresses of the ChamSys MagicQ for the light cues.

    `/pb/<playback>/<cue>` makes the playback jump directly to the cue, so every
    light effect triggers its own pre-programmed cue, independent of the order
    the cues are played in. The message needs no arguments.
    See https://docs.chamsys.co.uk/magicq/1.9.9.x/manual/OSC.html
    """

    def __init__(self, playback: int):
        if not FIRST_PLAYBACK <= playback <= LAST_PLAYBACK:
            raise ValueError(f"The MagicQ playback {playback} is outside of {FIRST_PLAYBACK}-{LAST_PLAYBACK}, "
                             f"which are the only ones controllable via OSC.")
        self.playback = playback

    def jump_to_cue_path(self, cue_number: int) -> str:
        return f"/pb/{self.playback}/{cue_number}"
