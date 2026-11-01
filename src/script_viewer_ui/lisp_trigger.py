import socket

from osc_routing.deck_routes import LISP_CUE_ADDRESS
from osc_routing.osc_message import osc_message


class LispTrigger:
    """Starts a LiSP cue by its user number (from 1) with an OSC message over UDP."""

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def trigger(self, host: str, port: int, cue_number: int) -> None:
        """Raises OSError if the message cannot be sent, e.g. because the host is unknown."""
        self._socket.sendto(osc_message(LISP_CUE_ADDRESS, cue_number), (host, port))
