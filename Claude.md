# Project Context

When working with this codebase, prioritize readability over cleverness. 
Ask clarifying questions before making architectural changes.

## About This Project

This project is used to automatically read the textbook of a theater from a PDF file and parse it into a structured data
format.
The source code is written in python.
The data format contains all characters and the entire textbook in one single dataset. 
Additional commands for light and sound are to be added into the dataset together with the text.
Each action, no matter if it is some text an actor says or some action the tech people need to perform, is represented
as a block in the data format.
The format (dataset) shall then be saved in a json or parquet file.

## Key Directories

- `src/` - Source code of the application
- `in/` - Input files, such as the textbook. NEVER READ THESE FILES!!! They are under copyright protection.
- `out/` - Output files. That is where the output dataset shall land. NEVER READ THESE FILES!!! They are under copyright protection.
- `.venv/` - python virtual environment

## Standards

- Clean code first!
- NEVER EVER read any files that are copyright protected. Reading files from `in/` or `out/` is considered to be a 
  crime. Example files will be provided instead.