import sys
import time

from serial import Serial

DEFAULT_BAUD_RATE = 9600
KEY_PREFIX = "KEY:"
# The Arduino resets when the port is opened and needs a moment before it sends anything.
ARDUINO_RESET_DELAY = 2
# How long read_index() waits for a line, so a reading loop can be stopped in time.
READ_TIMEOUT = 1


class ArduinoInterface:
    """Reads the button indices the Arduino sends over the serial port."""

    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        self.serial: Serial | None = None

    def __enter__(self) -> "ArduinoInterface":
        self.serial = Serial(self.port, self.baud_rate, timeout=READ_TIMEOUT)
        time.sleep(ARDUINO_RESET_DELAY)
        return self

    def __exit__(self, *exc_info) -> None:
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def read_index(self) -> int | None:
        line = self.serial.readline().decode("utf-8", errors="replace").strip()
        if not line.startswith(KEY_PREFIX):
            return None
        payload = line[len(KEY_PREFIX):]
        if not payload.isdigit():
            print(f"Ignoring malformed line from Arduino: '{line}'", file=sys.stderr)
            return None
        return int(payload)
