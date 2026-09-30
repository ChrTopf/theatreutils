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
   the live theater show.

The source code of all applications is written in python. For graphical applications the pyqt library must be used.


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