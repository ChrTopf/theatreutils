from dataclasses import dataclass

# OSC strings are terminated by at least one null byte and padded to a multiple of 4 bytes.
OSC_ALIGNMENT = 4
BUNDLE_MARKER = b"#bundle"


@dataclass
class RoutedPacket:
    route: str
    packet: bytes


class OscRouter:
    """Decides which deck an OSC message is for and strips the route from its address.

    The first address segment names the route: "/x32/-action/gosnippet" goes to
    the route "x32" as "/-action/gosnippet". Everything after the address (the
    type tags and arguments) is passed on byte for byte, so the router does not
    need to understand the arguments.
    """

    def __init__(self, routes: set[str]):
        self.routes = routes

    def route(self, packet: bytes) -> RoutedPacket:
        if packet.startswith(BUNDLE_MARKER):
            raise ValueError("OSC bundles are not supported.")
        address, rest = self._split_address(packet)

        _, route, *deck_segments = address.split("/")
        if route not in self.routes:
            raise ValueError(f"Unknown route '{route}' in OSC address '{address}'.")
        if not deck_segments:
            raise ValueError(f"The OSC address '{address}' contains no address for the deck.")

        deck_address = "/" + "/".join(deck_segments)
        return RoutedPacket(route, self._osc_string(deck_address) + rest)

    @staticmethod
    def _split_address(packet: bytes) -> tuple[str, bytes]:
        if not packet.startswith(b"/"):
            raise ValueError("The packet is no OSC message, its address does not start with '/'.")
        end = packet.find(b"\0")
        if end == -1:
            raise ValueError("The OSC address is not null terminated.")
        padded_length = (end // OSC_ALIGNMENT + 1) * OSC_ALIGNMENT
        return packet[:end].decode("ascii"), packet[padded_length:]

    @staticmethod
    def _osc_string(text: str) -> bytes:
        encoded = text.encode("ascii") + b"\0"
        padding = -len(encoded) % OSC_ALIGNMENT
        return encoded + b"\0" * padding
