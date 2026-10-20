#!/usr/bin/env python3
"""
Turn the buttons of an Arduino buzzer into key presses on this machine.

The Arduino does not send the key to press. It sends the index of the button
that was pressed, one line per press:

    KEY:<index>

The index is mapped to a key here, so the same buzzer can trigger different
keys without reflashing it. The mapping defaults to DEFAULT_KEY_MAP and can be
overridden per index with --key. Keys are either a single character or the name
of a special key of pynput (space, enter, esc, f1, page_down, ...).

If --port or --baud is omitted, the program asks for it interactively.

Usage:  python3 serial_keyboard.py --port /dev/ttyUSB0 --baud 9600 --key 1=space --key 2=f5
"""

import sys
import time
from argparse import ArgumentParser, ArgumentTypeError, Namespace

from pynput.keyboard import Controller, Key
from serial import Serial, SerialException
from serial.tools.list_ports import comports

DEFAULT_BAUD_RATE = 9600
KEY_PREFIX = "KEY:"
# The Arduino resets when the port is opened and needs a moment before it sends anything.
ARDUINO_RESET_DELAY = 2

DEFAULT_KEY_MAP: dict[int, str] = {
    0: "space",
    1: "1",
    2: "2",
    3: "3",
}


def parse_key(name: str) -> Key | str:
    if len(name) == 1:
        return name
    try:
        return Key[name.lower()]
    except KeyError:
        raise ArgumentTypeError(f"'{name}' is neither a single character nor a special key of pynput.") from None


def index_and_key(text: str) -> tuple[int, str]:
    index, separator, key = text.partition("=")
    if not separator or not index.isdigit() or not key:
        raise ArgumentTypeError(f"'{text}' is not of the form <index>=<key>.")
    parse_key(key)
    return int(index), key


class ArduinoInterface:
    """Reads the button indices the Arduino sends over the serial port."""

    def __init__(self, port: str, baud_rate: int):
        self.port = port
        self.baud_rate = baud_rate
        self.serial: Serial | None = None

    def __enter__(self) -> "ArduinoInterface":
        self.serial = Serial(self.port, self.baud_rate, timeout=1)
        time.sleep(ARDUINO_RESET_DELAY)
        return self

    def __exit__(self, *exc_info) -> None:
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def read_index(self) -> int | None:
        """Waits up to the read timeout for a key line and returns its index, or None."""
        line = self.serial.readline().decode("utf-8", errors="replace").strip()
        if not line.startswith(KEY_PREFIX):
            return None
        payload = line[len(KEY_PREFIX):]
        if not payload.isdigit():
            print(f"Ignoring malformed line from Arduino: '{line}'")
            return None
        return int(payload)


class KeyMapper:
    """Maps the button indices of the Arduino to keys and presses them."""

    def __init__(self, key_map: dict[int, str]):
        self.key_map = {index: parse_key(name) for index, name in key_map.items()}
        self.keyboard = Controller()

    def press(self, index: int) -> None:
        key = self.key_map.get(index)
        if key is None:
            print(f"No key mapped to index {index}.")
            return
        self.keyboard.press(key)
        self.keyboard.release(key)
        print(f"Index {index}: pressed {key_name(key)}")

    def describe(self) -> str:
        return "\n".join(f"  {index} -> {key_name(key)}" for index, key in sorted(self.key_map.items()))


def key_name(key: Key | str) -> str:
    return key.name if isinstance(key, Key) else f"'{key}'"


def choose_port() -> str:
    ports = sorted(comports(), key=lambda port_info: port_info.device)
    if not ports:
        print("No serial ports found.")
        sys.exit(1)

    print("Available ports:")
    for number, port_info in enumerate(ports, start=1):
        print(f"  [{number}] {port_info.device}: {port_info.description}")

    while True:
        choice = input(f"Choose a port [1-{len(ports)}]: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(ports):
            return ports[int(choice) - 1].device
        print("Invalid choice.")


def choose_baud_rate() -> int:
    while True:
        choice = input(f"Baud rate [{DEFAULT_BAUD_RATE}]: ").strip()
        if not choice:
            return DEFAULT_BAUD_RATE
        if choice.isdigit():
            return int(choice)
        print("Invalid baud rate.")


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--port", help="The serial port of the Arduino, e.g. /dev/ttyUSB0 or COM3 (asked for if omitted).", type=str)
    parser.add_argument("--baud", help=f"The baud rate of the serial connection (asked for if omitted, default {DEFAULT_BAUD_RATE}).", type=int)
    parser.add_argument("--key", help="Maps a button index to a key, e.g. 1=space or 2=a. Can be repeated and overrides the default mapping.", type=index_and_key, action="append", default=[])
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    port = arguments.port or choose_port()
    baud_rate = arguments.baud or choose_baud_rate()
    key_mapper = KeyMapper(DEFAULT_KEY_MAP | dict(arguments.key))

    print(f"Connecting to Arduino on {port} at {baud_rate} baud...")
    try:
        with ArduinoInterface(port, baud_rate) as arduino:
            print("Connected! Key mapping:")
            print(key_mapper.describe())
            print("Press Ctrl+C to exit")
            while True:
                index = arduino.read_index()
                if index is not None:
                    key_mapper.press(index)
    except SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
