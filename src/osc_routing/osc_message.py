import struct

# OSC strings are terminated by at least one null byte and padded to a multiple of 4 bytes.
OSC_ALIGNMENT = 4


def osc_string(text: str) -> bytes:
    encoded = text.encode("ascii") + b"\0"
    padding = -len(encoded) % OSC_ALIGNMENT
    return encoded + b"\0" * padding


def osc_message(address: str, *integers: int) -> bytes:
    """Encodes an OSC message with 32 bit integer arguments, e.g. `/lisp/cue ,i 5`."""
    type_tags = "," + "i" * len(integers)
    return osc_string(address) + osc_string(type_tags) + b"".join(struct.pack(">i", value) for value in integers)
