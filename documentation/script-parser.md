# Script Parser

`src/script_parser.py` is the first step of the show preparation. It reads the textbook of the play from a PDF file,
splits it into blocks, calculates when the microphone of every actor has to be muted and unmuted, and writes the result
to an Excel workbook.

The workbook is meant to be proof-read and enriched by hand (audio and light effects) before it is handed over to the
[Cue Generator](cue-generator.md).

```
textbook.pdf ─┐
              ├─► script_parser.py ─► workbook.xlsx ─► (manual editing) ─► cue_generator.py
characters.json ┘
```

## Requirements

- Python 3.10 or newer
- `pypdf` and `openpyxl` (see `requirements.txt`)
- The PDF must be text based. Scanned PDFs contain no text layer and yield no blocks.

## Usage

```shell
python3 src/script_parser.py --input textbook.pdf --output workbook.xlsx --characters characters.json
```

A typical call for a textbook with a title page, a page header and a page number in the footer:

```shell
python3 src/script_parser.py \
    --input textbook.pdf \
    --output workbook.xlsx \
    --characters characters.json \
    --startpage 3 \
    --trim-first-line \
    --trim-last-line \
    --threshold-turns 20 \
    --unmute-padding 2
```

## Command line arguments

| Argument | Required | Default | Description |
| - | - | - | - |
| `--input <file>` | yes | | The textbook as PDF file. |
| `--output <file>` | yes | | The workbook (`.xlsx`) to write. An existing file is overwritten. |
| `--characters <file>` | yes | | The `characters.json` file assigning actors, microphones and characters (see below). |
| `--startpage <n>` | no | `1` | The first page (counted from 1) that is parsed. Use it to skip title pages, the table of contents or the cast list. |
| `--trim-first-line` | no | off | Removes the first line of every page, e.g. a page header. |
| `--trim-last-line` | no | off | Removes the last line of every page, e.g. a page number. |
| `--threshold-turns <n>` | no | `20` | The minimum number of blocks an actor must stay silent before their microphone is muted in between two of their lines. A scene change mutes actors regardless of this value (see [Microphone annotation](#microphone-annotation)). |
| `--unmute-padding <n>` | no | `2` | The number of blocks an actor is unmuted before they speak. |
| `-h`, `--help` | no | | Prints the help and exits. |

## The characters file

The characters file tells the parser which character names exist in the play, which actor plays them and which
microphone channel on the audio deck belongs to that actor. An actor can play several characters, they share one
microphone channel.

```json
[
    {
        "mic": 1,
        "actor": "Herbert",
        "characters": [
            {"name": "Manfred", "actions": 1},
            {"name": "Dieter", "actions": 1}
        ]
    },
    {
        "mic": 2,
        "actor": "Günter",
        "characters": [
            {"name": "Polizist", "actions": 1}
        ]
    }
]
```

| Key | Description |
| - | - |
| `mic` | The input channel (1-32) of the actor's microphone on the Behringer X32. |
| `actor` | The real name of the actor. The mute / unmute annotations refer to this name. |
| `characters[].name` | The name of the character exactly as it is written in the textbook. |
| `characters[].actions` | Informational only, it is copied to the `Actions` column of the Characters sheet. |

An example can be found in `examples/characters.json`.

## How the textbook is parsed

The text of all pages (starting at `--startpage`) is concatenated and processed line by line, so dialogue and stage
directions spanning a page break end up in one block. Every line is trimmed. The parser recognizes the following
elements of a (German) textbook:

| Line in the textbook | Meaning | Result |
| - | - | - |
| `Vorspann` | The opening before the first act | Starts the part `Vorspann` (the initial part) |
| `1. Akt`, `2. Akt`, ... | Start of an act | Starts a new part |
| `1. Szene`, `2. Szene`, ... | Start of a scene | Starts a new scene within the current part |
| A line right after a scene heading listing only known character names, separated by commas | The characters present in the scene | An `acting` block |
| `Vorhang` | Curtain | A `command` block |
| `<Character>:` or `<Character>: (<direction>)` | A known character starts to speak | A `dialogue` block. The following lines up to the next blank line or the next character cue form its text. The text in brackets becomes the `Direction` |
| Any other paragraph | A stage direction | A `command` block if it contains one of the tech keywords below, otherwise an `acting` block. A paragraph ends at a blank line, a heading, a curtain or a character cue |

A character cue is only recognized if the name is listed in the characters file. Names that are missing or spelled
differently end up as stage directions, so the characters file should be checked first if dialogue is missing in the
workbook.

The tech keywords (case-insensitive, whole words only) are: `licht`, `beleuchtung`, `spot`, `verdunkelung`,
`blackout`, `ton`, `musik`, `sound`, `geräusch`, `einspieler`, `nebel`. They are defined in
`src/textbook_parser/line_classifier.py`.

Blocks are numbered from 0 in the order of the textbook. Every block remembers the page it starts on.

## Microphone annotation

After parsing, the parser decides when each actor's microphone is switched. Only `dialogue` blocks count as speaking.
The rules are applied per actor, i.e. all characters of an actor count as that actor speaking:

1. Every actor starts muted.
2. An actor is unmuted `--unmute-padding` blocks before their first line (at the earliest at the first block).
3. After a line, the actor is muted again if
   - they stay silent for at least `--threshold-turns` blocks: they are muted in the block right after their line, or
   - a new scene starts before their next line and they do not speak in the scene of that next line: they are muted
     at the first block of the new scene.
4. If they were muted, they are unmuted again `--unmute-padding` blocks before their next line.
5. A mute is dropped if the actor would have to be unmuted again at or before that very block, so a microphone is
   never switched off and on at once.
6. After their last line the same rules apply as if the actor spoke again far after the end of the play, so everybody
   is muted eventually.

The annotations are written to the `Mute` and `Unmute` columns as comma separated actor names.

Increasing `--threshold-turns` results in fewer mic changes (and fewer X32 snippets, of which the console holds 100
per show). Decreasing it mutes actors more aggressively.

## Output

The workbook contains two sheets. Their columns are described in the README section
[Excel Workbook Format](../README.md#excel-workbook-format).

- **Characters**: one row per character with `Mic`, `Actor`, `Character` and `Actions`. The `Mic` and `Actor` cells of
  an actor playing several characters are merged.
- **Blocks**: one row per block with `ID`, `Part`, `Scene`, `Page`, `Type`, `Character`, `Direction`, `Text`, `Mute`
  and `Unmute`. The rows are shaded per scene, a thin line marks a new scene and a thick line a new part. Commands are
  printed in bold red, acting in grey italics.

The columns `Audio Effect` and `Light` are **not** written by the parser. Add them by hand (the header names must match
exactly) and fill in the name of the audio file (without `.wav`) and the light effect of the blocks that trigger them.
Any further columns are ignored by the cue generator, the order of the columns does not matter.

While proof-reading, mute and unmute annotations, characters and texts may be corrected freely. The `ID` column must
stay filled for every block, rows without an ID are ignored by the cue generator.
