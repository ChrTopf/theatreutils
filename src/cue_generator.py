#!/usr/bin/env python3
"""
Generate the cues for the decks from a workbook produced by script_parser.py
(optionally enriched by hand).

- One Behringer X32 snippet (.snp) per block that mutes or unmutes actors. The
  microphone channel of each actor is taken from the Characters sheet.
- Optionally a Linux Show Player project (.lsp) with cues for the mic changes
  (recalling the X32 snippets via OSC), the audio effects and the light effects
  (MSC GO to the ChamSys MagicQ). `--lisp-mutes`, `--lisp-audio` and
  `--lisp-light` select which cues land in it.
- Optionally a CSV list of the light cues that must be programmed into the MagicQ.

Install dependency:  pip install openpyxl
Usage:               python3 cue_generator.py --input blocks.xlsx --snp-output-dir snippets --theater-name Hugo \
                         --lisp-output Hugo.lsp --lisp-mutes --lisp-audio --lisp-light --light-output light_cues.csv
"""

import sys
from argparse import ArgumentParser, Namespace

from light_cue_assigner import LightCueAssigner
from light_cue_list_writer import LightCueListWriter
from lisp_cue_factory import LispCueFactory
from lisp_project_builder import LispProjectBuilder
from lisp_project_writer import LispProjectWriter
from midi_show_control import ALL_CALL_DEVICE_ID, MidiShowControl
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
    parser.add_argument("--lisp-output", help="The Linux Show Player project file (.lsp) to write. The audio files are expected next to it.", type=str)
    parser.add_argument("--lisp-mutes", help="Add a cue recalling the X32 snippet for every mic change to the lisp project.", action="store_true")
    parser.add_argument("--lisp-audio", help="Add a cue playing <Audio Effect>.wav for every audio effect to the lisp project.", action="store_true")
    parser.add_argument("--lisp-light", help="Add an MSC GO cue to the MagicQ for every light effect to the lisp project.", action="store_true")
    parser.add_argument("--light-output", help="The CSV file listing the light cues to program into the MagicQ.", type=str)
    parser.add_argument("--msc-device-id", help=f"The MSC device id of the MagicQ (default: {ALL_CALL_DEVICE_ID}, all devices).", type=int, default=ALL_CALL_DEVICE_ID)
    parser.add_argument("--magicq-playback", help="The MagicQ playback (MSC cue list) holding the light cues (default: 1).", type=int, default=1)
    args = parser.parse_args()

    lisp_selected = args.lisp_mutes or args.lisp_audio or args.lisp_light
    if lisp_selected and not args.lisp_output:
        parser.error("--lisp-mutes, --lisp-audio and --lisp-light require --lisp-output.")
    if args.lisp_output and not lisp_selected:
        parser.error("--lisp-output requires at least one of --lisp-mutes, --lisp-audio and --lisp-light.")
    return args


if __name__ == "__main__":
    args = parse_arguments()
    importer = WorkbookImporter()
    actors = importer.import_actors(args.input)
    blocks = importer.import_blocks(args.input)

    snippet_builder = SnippetBuilder()
    try:
        snippets = snippet_builder.build(actors, blocks)
        msc = MidiShowControl(args.msc_device_id, args.magicq_playback)
    except ValueError as error:
        sys.exit(f"Error: {error}")

    if len(snippets) > MAX_SNIPPET_COUNT:
        print(f"Warning: {len(snippets)} snippets were generated, but the X32 only holds {MAX_SNIPPET_COUNT} per show.",
              file=sys.stderr)

    paths = SnippetWriter().write(snippets, args.snp_output_dir, args.theater_name)
    print(f"Wrote {len(paths)} snippets to '{args.snp_output_dir}'.")

    light_cue_numbers = LightCueAssigner().assign(blocks)
    if args.light_output:
        LightCueListWriter().write(light_cue_numbers, blocks, args.light_output)
        print(f"Wrote {len(light_cue_numbers)} light cues to '{args.light_output}'.")

    if args.lisp_output:
        project = LispProjectBuilder(
            LispCueFactory(), msc, snippet_builder.snippet_numbers(blocks), light_cue_numbers,
            include_mutes=args.lisp_mutes, include_audio=args.lisp_audio, include_light=args.lisp_light,
        ).build(blocks)
        LispProjectWriter().write(project, args.lisp_output)
        print(f"Wrote {len(project['cues'])} cues to '{args.lisp_output}'.")
