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

The source code of all applications is written in python. For graphical applications the pyqt library must be used.

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