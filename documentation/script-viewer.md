# Script Viewer

`src/script_viewer.py` displays the script exported by the [Cue Generator](cue-generator.md) during the live show. It
shows the text block by block together with the mic, audio and light actions and, in colored lanes next to it, the LiSP
cues, X32 snippets and light cues generated for every block. The operator follows the performance by moving from block
to block and always sees which cue comes next.

## Requirements

- Python 3.10 or newer
- `PyQt5` (see `requirements.txt`)

## Usage

```shell
python3 src/script_viewer.py --input out/Hugo.json
```

Without `--input` a file dialog asks for the script. Cancelling the dialog quits the program.

## Command line arguments

| Argument | Required | Default | Description |
| - | - | - | - |
| `--input <file>` | no | file dialog | The script (`.json`) written by the cue generator with `--script-output`. |
| `-h`, `--help` | no | | Prints the help and exits. |

The program exits with an error message if the file cannot be read or is not a script of format version 1.

## The window

The window opens maximized and is titled `Script Viewer - <file name>`.

### Top bar

| Element | Description |
| - | - |
| `Part` selector | Jumps to the first scene of the chosen part (`Vorspann`, `1. Akt`, ...). |
| `Scene` selector | Jumps to the first block of the chosen scene within the selected part. |
| Lane buttons | `LiSP Cues`, `X32 Snippets` and `Light Cues` show or hide the corresponding lane. A visible lane's button is outlined in the lane's color, a hidden one is grey. Hidden lanes make room for wider text. |
| Position | `Page <page> · Block <n> / <total>` of the current block. |

Both selectors follow the current block, so they always show where in the show it is located.

### Block cards

Every block is shown as a card. The current block is always centered vertically, drawn brightly and outlined; all other
blocks are dimmed.

- The left column shows the character name in capitals above the text. A stage direction of a dialogue is shown in
  brackets and italics before the text. `acting` blocks are printed in italics, `command` blocks in bold.
- The right column lists the actions of the block:

  | Symbol | Meaning |
  | - | - |
  | `▲ <actor>` | Unmute the actor's microphone |
  | `▼ <actor>` | Mute the actor's microphone |
  | `♪ <effect>` | Play the audio effect |
  | `☀ <effect>` | Trigger the light effect |

### Cue lanes

Right of the cards, one lane per deck shows which cue is active. A colored bar starts at the block triggering a cue and
runs down to the block triggering the next cue of that deck. Neighbouring cues have different colors. The name of the
cue is written in large bold letters beside the start of its bar. It consists of a letter and a three digit number,
longer names are cut to four characters:

| Lane | Label |
| - | - |
| LiSP Cues | `L<number>`, e.g. `L001` |
| X32 Snippets | `S<number>`, e.g. `S001` |
| Light Cues | `Q<number>`, e.g. `Q001` |

If a block triggers several cues of one deck, all of their names are listed.

Below the document, a fixed strip shows the next cue of every visible lane under that lane, in the color its bar will
have. It stays in place while scrolling, so the upcoming cues are always visible. If a block triggers several cues of
one deck, the first one is shown; if no cue follows in a lane, `—` is shown. Hiding all lanes also hides the strip.

## Navigation

| Input | Action |
| - | - |
| Scroll wheel | One block forward / back per notch (touchpad deltas are accumulated) |
| `↓`, `→`, `Space` | Next block |
| `↑`, `←`, `Backspace` | Previous block |
| `Page Down` / `Page Up` | Ten blocks forward / back |
| `Home` / `End` | First / last block |
| Mouse click | Makes the clicked block the current one |
| Part / scene selectors | Jump to a scene |

The script document keeps the keyboard focus after using the selectors or the lane buttons, so the keys keep working.

Note that the Space key is also LiSP's default GO key. If the [Buzzer](buzzer.md) is used to trigger LiSP via the
[Serial Keyboard](serial-keyboard.md), the key press goes to whichever window has the focus, so keep LiSP focused
during the show.
