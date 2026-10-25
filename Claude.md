# Project Context

When working with this codebase, prioritize readability over cleverness. 
Ask clarifying questions before making architectural changes.
Never ever execute any commands! This is a major cybersecurity concern. 
Every command which you execute is going to be rejected.

## About This Project

This project contains multiple utility programs to prepare and conduct theater shows.
The source code of all applications is written in python. 
For graphical applications the pyqt5 library must be used.

The documentation of this project can be found in README.md

## Key Directories

- `src/` - Source code of the applications
- `in/` - Input files, such as the textbook. NEVER READ THESE FILES!!! They are under copyright protection.
- `out/` - Output files. That is where the output dataset shall land. NEVER READ THESE FILES!!! They are under copyright protection.
- `examples/` - Example files for each format used by the applications.
- `.venv/` - python virtual environment
- `documentation/` - contains all documentation files

## Standards

- Clean code first!
- NEVER EVER read any files that are copyright protected. Reading files from `in/` or `out/` is considered to be a 
  crime. Example files will be provided instead.

## Applications

- `src/script_parser.py` The first program which parses the textbook from PDF and extracts all blocks.
- `src/script_viewer.py` The second program which displays the script (JSON) exported by the cue generator during the live show. Its UI classes live in `src/script_viewer_ui/`.
- `src/cue_generator.py` The third program which generates the deck cues and the script (JSON) from the workbook.
- `src/osc_relay.py` Runs during the show and forwards the OSC messages of LiSP to the X32 and the MagicQ.
