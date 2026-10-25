# Serial Keyboard

`src/serial_keyboard.py` receives the button presses of the [Buzzer](buzzer.md) over a serial port and executes one
shell command for each of them on the machine it runs on.

## Requirements

- Python 3.10 or newer
- `pyserial` (see `requirements.txt`)
- Read and write access to the serial port. On Linux, the user usually has to be a member of the `uucp` or `dialout`
  group, depending on the distribution.

## Usage

```shell
python3 src/serial_keyboard.py --port /dev/ttyUSB0 --baud 9600 --command "notify-send GO"
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
| `--command <command>` | yes | | The shell command executed on every button press. |
| `-h`, `--help` | no | | Prints the help and exits. |

### Command

The command is passed to the system shell (`/bin/sh` on Linux), so pipes, redirections and `&&` work. Quote it so
your own shell passes it unchanged:

```shell
python3 src/serial_keyboard.py --command "echo pressed >> buzzer.log"
```

## Startup

1. It opens the serial port and waits two seconds, because the Arduino resets when the port is opened.
2. It prints the command.

```
Connecting to Arduino on /dev/ttyACM0 at 9600 baud...
Connected! Command: notify-send GO
Press Ctrl+C to exit
```

## Behaviour

- Every line `KEY:<index>` received from the Arduino starts the command and prints `Executed '<command>'`. The index
  is ignored, so every buzzer triggers the same command.
- The command runs in the background. The program does not wait for it to finish, so further button presses are
  handled immediately, even while a previous command is still running. Its output goes to the terminal of the program.
- Lines with a non-numeric index are reported and ignored, all other lines are ignored silently.
- If the serial connection fails or is lost (e.g. the Arduino is unplugged), the program exits with
  `Serial error: ...` and exit code 1.
