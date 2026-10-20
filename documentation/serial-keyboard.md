# Serial Keyboard

`src/serial_keyboard.py` receives the button presses of the [Buzzer](buzzer.md) over a serial port and turns them into
key presses on the machine it runs on. During the show it is used to press the GO key (Space) of the
[Linux Show Player](lisp.md), so LiSP jumps to the next cue at the press of a physical button.

## Requirements

- Python 3.10 or newer
- `pyserial` and `pynput` (see `requirements.txt`)
- Read and write access to the serial port. On Linux, the user usually has to be a member of the `uucp` or `dialout`
  group, depending on the distribution.
- A session that allows synthetic key presses. On GNOME with Wayland, the system asks for the permission to control
  the input devices (see [Startup](#startup)).

## Usage

```shell
python3 src/serial_keyboard.py --port /dev/ttyUSB0 --baud 9600 --key 1=space
```

Without `--port` and `--baud` the program asks for them interactively:

```
Available ports:
  [1] /dev/ttyACM0: Arduino Uno
  [2] /dev/ttyUSB0: USB Serial
Choose a port [1-2]: 1
Baud rate [9600]:
```

Stop the program with `Ctrl+C`.

## Command line arguments

| Argument | Required | Default | Description |
| - | - | - | - |
| `--port <port>` | no | asked for | The serial port of the Arduino, e.g. `/dev/ttyUSB0`, `/dev/ttyACM0` or `COM3`. If omitted, all available ports are listed to choose from. |
| `--baud <rate>` | no | asked for (`9600`) | The baud rate of the serial connection. Must match the sketch, which uses 9600. If omitted, it is asked for; pressing Enter takes 9600. |
| `--key <index>=<key>` | no | see below | Maps a button index to a key. Can be repeated. Overrides the default mapping for that index, all other indices keep their default. |
| `-h`, `--help` | no | | Prints the help and exits. |

### Keys

A key is either

- a single character, e.g. `a`, `1` or `+`, or
- the name of a special key of [pynput](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key)
  (case-insensitive), e.g. `space`, `enter`, `esc`, `tab`, `backspace`, `up`, `down`, `left`, `right`, `page_up`,
  `page_down`, `home`, `end`, `f1` ... `f20`.

Invalid mappings are rejected at startup.

### Default mapping

| Index | Key |
| - | - |
| 0 | `space` |
| 1 | `1` |
| 2 | `2` |
| 3 | `3` |

The buzzer sketch sends index `1` by default, which is mapped to the key `1`. To press Space with an unmodified buzzer,
start the program with `--key 1=space`.

## Startup

1. The program presses `Esc` once. On GNOME this makes the system ask for the input permission right away instead of
   at the first button press during the show. Grant it.
2. It opens the serial port and waits two seconds, because the Arduino resets when the port is opened.
3. It prints the active key mapping.

```
Connecting to Arduino on /dev/ttyACM0 at 9600 baud...
Connected! Key mapping:
  0 -> space
  1 -> space
  2 -> '2'
  3 -> '3'
Press Ctrl+C to exit
```

## Behaviour

- Every line `KEY:<index>` received from the Arduino presses and releases the key mapped to the index and prints
  `Index <index>: pressed <key>`.
- Indices without a mapping are reported with `No key mapped to index <index>.`
- Lines with a non-numeric index are reported and ignored, all other lines are ignored silently.
- The key press goes to the window that currently has the keyboard focus. Keep LiSP focused during the show.
- If the serial connection fails or is lost (e.g. the Arduino is unplugged), the program exits with
  `Serial error: ...` and exit code 1.
