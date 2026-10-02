#!/usr/bin/env python3
"""
Generate the cues for the decks from a workbook produced by script_parser.py
(optionally enriched by hand).

For now this writes one Behringer X32 snippet (.snp) per block that mutes or
unmutes actors. The microphone channel of each actor is taken from the
Characters sheet of the workbook.

Install dependency:  pip install openpyxl
Usage:               python3 cue_generator.py --input blocks.xlsx --snp-output-dir snippets --theater-name Hugo
"""

import sys
from argparse import ArgumentParser, Namespace

from snippet_builder import SnippetBuilder
from snippet_writer import SnippetWriter
from workbook_importer import WorkbookImporter

# The X32 holds snippets 000 to 099 per show.
MAX_SNIPPET_COUNT = 100


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The workbook file (.xlsx) containing the Characters and Blocks sheets.", type=str, required=True)
    parser.add_argument("--snp-output-dir", help="The directory the X32 snippet files (.snp) are written to.", type=str, required=True)
    parser.add_argument("--theater-name", help="The name of the theater piece, used as prefix of the snippet file names.", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    importer = WorkbookImporter()
    actors = importer.import_actors(args.input)
    blocks = importer.import_blocks(args.input)

    try:
        snippets = SnippetBuilder().build(actors, blocks)
    except ValueError as error:
        sys.exit(f"Error: {error}")

    if len(snippets) > MAX_SNIPPET_COUNT:
        print(f"Warning: {len(snippets)} snippets were generated, but the X32 only holds {MAX_SNIPPET_COUNT} per show.",
              file=sys.stderr)

    paths = SnippetWriter().write(snippets, args.snp_output_dir, args.theater_name)
    print(f"Wrote {len(paths)} snippets to '{args.snp_output_dir}'.")
