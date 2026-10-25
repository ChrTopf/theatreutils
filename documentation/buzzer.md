# Buzzer

`src/buzzer/buzzer.ino` is a small Arduino sketch that sends a line over the serial (USB) connection whenever a
physical button is pressed. Together with the [Serial Keyboard](serial-keyboard.md) it turns the button into a shell
command executed on the show computer.

```
Button ──► Arduino (buzzer.ino) ──"KEY:1"──► serial_keyboard.py ──► shell command
```

## Command line arguments

The buzzer is an Arduino sketch and has no command line arguments. It is configured with the constants at the top of
the sketch, which take effect after flashing it again:

| Constant | Default | Description |
| - | - | - |
| `BUTTON_PIN` | `0` | The digital pin the button is connected to. The internal pull-up is enabled, so the button connects the pin to GND. |
| `LED_PIN` | `2` | The digital pin of a status LED. |
| `KEY_INDEX` | `1` | The index sent when the button is pressed. The Serial Keyboard ignores it. |
| `DEBOUNCE_DELAY` | `50` | The time in milliseconds the button state must be stable before a press is accepted. |

The serial connection runs at 9600 baud.

Note that on many AVR boards (e.g. Uno, Nano) pin 0 is the RX pin of the serial connection. On such boards, connect the
button to another pin and change `BUTTON_PIN` accordingly.

## Flashing

1. Open `src/buzzer/buzzer.ino` in the Arduino IDE (or use `arduino-cli`).
2. Select the board and its port.
3. Upload the sketch.

## Wiring

- One contact of the button to `BUTTON_PIN`, the other to GND. No external resistor is needed.
- Optionally an LED with a series resistor from `LED_PIN` to GND.

## Protocol

Every accepted button press sends one line terminated by `\r\n`:

```
KEY:<KEY_INDEX>
```

The press is detected when the button is pressed down, releasing it sends nothing. Holding the button sends one line
only.

The sketch does not send the command itself. Which command is executed is decided by the Serial Keyboard with
`--command`, so the buzzer can trigger a different command without reflashing it.

## LED

The LED is switched on when the sketch starts. With every button press it is switched on and immediately off again,
so it stays off after the first press.
