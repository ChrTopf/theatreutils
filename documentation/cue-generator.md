# Cue Generator

`src/cue_generator.py` is the second step of the show preparation. It reads the workbook written by the
[Script Parser](script-parser.md), after it has been proof-read and enriched with audio and light effects, and generates
everything needed to program the decks and to follow the show:

| Output | Argument | Used by |
| - | - | - |
| Behringer X32 snippets (`.snp`), one per mic change | `--snp-output-dir` (always written) | X32 / X32-Edit |
| Linux Show Player project (`.lsp`) | `--lisp-output` | [LiSP](lisp.md) |
| List of light cues to program (`.csv`) | `--light-output` | Light designer / ChamSys MagicQ |
| Script (`.json`) | `--script-output` | [Script Viewer](script-viewer.md) |

## Requirements

- Python 3.10 or newer
- `openpyxl` (see `requirements.txt`)

## Usage

Only the snippets:

```shell
python3 src/cue_generator.py --input workbook.xlsx --snp-output-dir snippets --theater-name Hugo
```

Everything:

```shell
python3 src/cue_generator.py \
    --input workbook.xlsx \
    --snp-output-dir out/scenes \
    --theater-name Hugo \
    --lisp-output out/Hugo.lsp --lisp-mutes --lisp-audio --lisp-light \
    --magicq-playback 1 \
    --light-output out/light-cues.csv \
    --script-output out/Hugo.json
```

The program prints a summary of the written files. Existing files are overwritten, missing output directories are
created.

## Command line arguments

| Argument | Required | Default | Description |
| - | - | - | - |
| `--input <file>` | yes | | The workbook (`.xlsx`) with the `Characters` and `Blocks` sheets. |
| `--snp-output-dir <dir>` | yes | | The directory the X32 snippets are written to. |
| `--theater-name <name>` | yes | | The name of the play, used as prefix of the snippet file names (`<name>.001.snp`). |
| `--lisp-output <file>` | no | | The Linux Show Player project (`.lsp`) to write. Requires at least one of `--lisp-mutes`, `--lisp-audio` and `--lisp-light`. |
| `--lisp-mutes` | no | off | Adds a cue recalling the X32 snippet of every mic change to the LiSP project. Requires `--lisp-output`. |
| `--lisp-audio` | no | off | Adds a cue playing `<Audio Effect>.wav` for every audio effect to the LiSP project. Requires `--lisp-output`. |
| `--lisp-light` | no | off | Adds a cue jumping to the light effect's cue on the MagicQ for every light effect to the LiSP project. Requires `--lisp-output`. |
| `--magicq-playback <n>` | no | `1` | The MagicQ playback (1-10) holding the light cues. Only the first 10 playbacks can be controlled via OSC. |
| `--light-output <file>` | no | | The CSV file listing the light cues that must be programmed into the MagicQ. |
| `--script-output <file>` | no | | The script (`.json`) for the Script Viewer. |
| `-h`, `--help` | no | | Prints the help and exits. |

The `--lisp-*` flags and `--lisp-output` must be given together, otherwise the program exits with an error message.

## Input

The workbook format is described in the README section [Excel Workbook Format](../README.md#excel-workbook-format).
Columns are looked up by their header name, so their order does not matter and additional columns are ignored.

- **Characters** sheet: requires `Mic`, `Actor` and `Character`. A row without `Mic` and `Actor` belongs to the actor
  of the row above (this is how merged cells are read).
- **Blocks** sheet: requires `ID`, `Part`, `Scene`, `Page`, `Type` and `Text`. `Character`, `Direction`, `Mute`,
  `Unmute`, `Audio Effect` and `Light` are optional. Rows without an `ID` are skipped.

The `Mute` and `Unmute` cells contain comma separated actor names. Every name must be listed in the Characters sheet.

## Output

### X32 snippets

Every block that mutes or unmutes at least one actor yields one snippet. A snippet only contains the on/off switches
(`/ch/NN/mix/on`) of the microphone channels of the actors it mutes or unmutes, so recalling it leaves every other
channel and parameter of the console untouched. If an actor is muted and unmuted in the same block, the unmute wins.

- Files are named `<theater-name>.<3-digit-number>.snp` and numbered from `001` in the order of the play, just like
  X32-Edit names them. Non-ASCII characters are replaced by `?`.
- Snippets are named after their position in the play: `A<act>S<scene> B<block id>`, e.g. `A2S3 B415`. A part without
  a number uses its initial, e.g. `VS1 B4` for `Vorspann`.
- The X32 holds 100 snippets per show. If more are generated, a warning is printed to stderr (the files are written
  anyway). Raise `--threshold-turns` of the Script Parser or merge mic changes in the workbook to reduce the number.

An example is located at `examples/Hugo.037.snp`.

### Linux Show Player project

The project is written for LiSP 0.6.5 in the list layout. For every block, the following cues are generated in this
order, each one only if its flag is given and the block has the corresponding action:

| Flag | Cue type | Content |
| - | - | - |
| `--lisp-mutes` | OSC cue | `/x32/load ,siii "snippet" <slot> 0 0`: recalls the block's snippet on the X32. The slot is the snippet file number minus one, because the console counts its slots from 00. The description lists the muted and unmuted actors. |
| `--lisp-audio` | Media cue | Plays `<Audio Effect>.wav` (the extension is added if missing). The file is expected next to the `.lsp` file. |
| `--lisp-light` | OSC cue | `/mq/pb/<playback>/<cue>` without arguments: makes the MagicQ playback jump to the cue of the light effect. |

All cues of a block are named `<part> Scene <scene> Block <id>`. If a block has several cues, every cue but the last
one triggers the next one right away, so a single GO in LiSP executes all actions of the block.

LiSP sends all OSC messages to one host. The prefixes `/x32` and `/mq` tell the [OSC Relay](osc-relay.md) which deck a
message is for. The relay must be running during the show.

The X32 snippets have to be loaded into the show on the console (e.g. with X32-Edit) so that the slot numbers match.

### Light cue list

Every distinct light effect name of the `Light` column gets one MagicQ cue number, numbered from 1 in order of first
appearance. An effect used by several blocks reuses its cue, so it only has to be programmed once. The CSV has the
columns:

| Column | Description |
| - | - |
| `Cue` | The cue number on the MagicQ playback given by `--magicq-playback` |
| `Effect` | The name of the light effect from the workbook |
| `Blocks` | Comma separated IDs of the blocks triggering the effect |

The cue numbers are assigned regardless of whether `--light-output` is given, so the LiSP project and the script always
use the same numbers for the same workbook.

### Script

The script contains all blocks together with the LiSP cues, X32 snippets and light cues, each referring to the
block(s) triggering it. Its format is described in the README section
[Script (JSON) Format](../README.md#script-json-format). The list of LiSP cues is empty if no `--lisp-output` is
given.

## Errors

The program exits with an error message (exit code 1) if

- a required sheet or column is missing in the workbook,
- an actor of the `Mute` / `Unmute` columns is not listed in the Characters sheet,
- a microphone channel is outside of 1-32,
- `--magicq-playback` is outside of 1-10, or
- the `--lisp-*` flags and `--lisp-output` are not given together (exit code 2).
