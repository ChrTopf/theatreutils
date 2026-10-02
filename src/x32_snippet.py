from dataclasses import dataclass, field

FORMAT_VERSION = "4.0"
CHANNEL_COUNT = 32

# Parameter category mask of the snippet header. Copied from the snippets generated
# for last year's show, in which 128 selects the channel on/mute switches only.
PARAMETER_MASK = 128

# The header line is padded with spaces to a fixed length, just like in the
# snippets generated for last year's show (128 bytes including the line feed).
HEADER_LENGTH = 127


@dataclass
class X32Snippet:
    """A Behringer X32 snippet that switches the on/mute state of some input channels.

    Recalling a snippet on the console changes only the channels it contains;
    every other channel and parameter keeps its current setting.
    """

    name: str
    channel_states: dict[int, bool] = field(default_factory=dict)

    def set_channel(self, channel: int, on: bool) -> None:
        if not 1 <= channel <= CHANNEL_COUNT:
            raise ValueError(f"Snippet '{self.name}': channel {channel} is outside of 1-{CHANNEL_COUNT}.")
        self.channel_states[channel] = on

    def channel_mask(self) -> int:
        """Bitmask of the contained channels, bit 0 being channel 1."""
        mask = 0
        for channel in self.channel_states:
            mask |= 1 << (channel - 1)
        return mask

    def to_text(self) -> str:
        header = f'#{FORMAT_VERSION}# "{self.name}" {PARAMETER_MASK} {self.channel_mask()} 0 0 1'
        lines = [header.ljust(HEADER_LENGTH)]
        for channel in sorted(self.channel_states):
            state = "ON" if self.channel_states[channel] else "OFF"
            lines.append(f"/ch/{channel:02d}/mix/on {state}")
        return "\n".join(lines) + "\n"
