# Project Context

When working with this codebase, prioritize readability over cleverness. 
Ask clarifying questions before making architectural changes.

## About This Project

This project contains multiple utility programs to prepare and conduct theater shows.
List of applications:

1. Script Parser: Reads the theater script from PDF file, calculates microphone mutes with the help of a json file and 
   parses the output into an excel workbook.
2. Script Viewer: Reads the output of the previous application which has been slightly modified and displays it in a 
   window together with mute annotations, audio and lighting commands. This application is intended to be used during 
   the live theater show to read through the text in parallel.
3. Cue generator: The last software in the chain which generates the cues for each deck. It takes the excel workbook as 
   an input and several output files.

The source code of all applications is written in python. For graphical applications the pyqt5 library must be used.

### The paradigm across all formats
The core philosophy of all formats handled by the applications builds on blocks.
Blocks are generated from the textbook PDF and represent everything that is happening during the show.
The blocks can later be converted into cues for some audio and light decks and displayed by the Script Viewer.

### Excel Workbook Format
The Excel workbook is produced by openpyxl and contains two Sheets:

- Characters
- Blocks

The Characters Sheet contains a table with the following columns:

| Column Name | Description |
| - | - |
| Mic | The assigned microphone channel on the audio deck |
| Actor | The real name of the actor |
| Character | The character played by the actor |
| Actions | The amount of actions of each actor according to the textbook |

If an actor plays multiple roles (characters) the table also contains multiple entries and one microphone channel is 
reused.

The Blocks Sheet contains a table with the following columns:

| Column Name | Data Type                      | Description                |
| - |--------------------------------|----------------------------|
| ID | int | The unique ID of the block |
| Part | string | The part of the entire Show. Preplay or specific Act |
| Scene | int | Current scene |
| Page | int | The page number of the block in the original PDF file |
| Type | string | The type of the block. Can be one of `command`, `acting` or `dialogue` |
| Character | string | The name of the character speaking or acting |
| Direction | string | What happens on stage |
| Text | string | What the character currently says on the stage |
| Mute | string | Comma separated list of actor names that must be muted during this block |
| Unmute | string | Comma separated list of actor names that must be unmuted during this block |
| Audio Effect | string | The name of the audio effect to be played during this block |
| Light | string | The name of the light effect to be played during this block |

The table can contain additional columns which shall be ignored if the textbook is imported.

### Cue Generator - Output files
The cue generator application takes the excel workbook as input. It uses both spreadsheets to perform its calculations 
and generate the output files.

#### Behringer X32 Scenes
Every time a block contains an actor to be muted / unmuted, another `.snp` file must be generated. The generated files 
must be stored in a directory which is given by the cli argument `--snp-output-dir`. Every file must follow the pattern 
`<theater-name>.<3-digit-number>.snp` which originally comes from the Behringer x32 edit application. The name of the
theater piece is given by the cli argument `--theater-name`. If the calculated number of scenes exceeds 100, a warning 
message needs to be generated.
An example of a generated file can be found in `examples/Hugo.037.snp`.

#### Lisp (Linux show player) project
The cue generator must also generate cues for the linux show player. The result is a complete `.lsp` project.
An example of such a json file is located at `examples/testcue 01.lsp`. Similar to the X32 scenes a new cue is
generated for every mute/unmute snippet, audio and light direction. The file names for the audio are the same as in 
the workbook ending with `.wav`. For the light there are preprogrammed cues in the chamsys magicq deck which just need 
to be triggered with an OSC cue. If one block contains multiple actions from mute/unmute, audio and light commands, 
three cues must be generated that are triggered at the same time. There are three command line options which determine
what lands in the lisp project: `--lisp-mutes`, `--lisp-audio` and `--lisp-light`.
The project is written to the file given by `--lisp-output`.

Connection to the decks (LiSP 0.6.5 sends all OSC cues to one global host, the OSC relay, see below). The first
address segment of every OSC cue names the target deck (`/x32/...` or `/mq/...`):
- Mute/unmute cues are OSC cues `/x32/-action/gosnippet <n>` that recall the X32 snippet with the same number as the
  generated `.snp` file. Snippets are numbered from 1.
- Audio cues are media cues playing `<Audio Effect>.wav`, which is expected next to the `.lsp` file.
- Light cues are OSC cues `/mq/pb/<playback>/<cue>` (no arguments) that make the ChamSys MagicQ jump to the cue
  (see https://docs.chamsys.co.uk/magicq/1.9.9.x/manual/OSC.html). The playback is set by `--magicq-playback`
  (1-10, default 1, only the first 10 playbacks are controllable via OSC).
  Every light effect name gets one MagicQ cue number (numbered from 1 in order of first appearance, reused if the
  effect occurs again). The list of cues to program into the desk is written as CSV (`Cue`, `Effect`, `Blocks`) to
  the file given by `--light-output`.
- No MIDI cues are generated: the MidiCue settings page of LiSP 0.6.5 crashes on SysEx (e.g. MSC) messages.

### OSC Relay
`src/osc_relay.py` receives the OSC messages of LiSP over UDP, removes the first address segment and forwards the
otherwise unchanged packet to the deck it names: `/x32/...` to `--x32 <host>:<port>` (the X32 listens on 10023),
`/mq/...` to `--magicq <host>:<port>` (the OSC receive port set on the MagicQ). It listens on `--listen-host`
(default 127.0.0.1) and `--listen-port` (default 9001, LiSP's default OSC destination).

## Key Directories

- `src/` - Source code of the applications
- `in/` - Input files, such as the textbook. NEVER READ THESE FILES!!! They are under copyright protection.
- `out/` - Output files. That is where the output dataset shall land. NEVER READ THESE FILES!!! They are under copyright protection.
- `examples/` - Example files for each format used by the applications.
- `.venv/` - python virtual environment

## Standards

- Clean code first!
- NEVER EVER read any files that are copyright protected. Reading files from `in/` or `out/` is considered to be a 
  crime. Example files will be provided instead.

## Applications

- `src/script_parser.py` The first program which parses the textbook from PDF and extracts all blocks.
- `src/script_viewer.py` The second program which displays the (enriched) workbook during the live show. Its UI classes live in `src/script_viewer_ui/`.
- `src/cue_generator.py` The third program which generates the deck cues from the workbook.
- `src/osc_relay.py` Runs during the show and forwards the OSC messages of LiSP to the X32 and the MagicQ.
