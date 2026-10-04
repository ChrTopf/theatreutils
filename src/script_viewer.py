#!/usr/bin/env python3
"""
Display the script exported by cue_generator.py to follow the text during the live show.

Next to the text and its mic, audio and light effects, the LiSP cues, X32
snippets and light cues generated for every block are shown in colored lanes.

Install dependency:  pip install pyqt5
Usage:               python3 script_viewer.py --input Hugo.json

Navigation:          scroll wheel / arrow keys / space   next or previous block
                     page up / page down                 ten blocks back or forward
                     home / end                          first or last block
                     mouse click                         jump to the clicked block
                     part / scene selectors              jump to a scene of a part
"""

import os
import sys
from argparse import ArgumentParser, Namespace

from PyQt5.QtWidgets import QApplication, QFileDialog

from model.script import Script
from script_viewer_ui import ScriptViewerWindow


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The script file (.json) written by cue_generator.py to display. A file dialog is shown if omitted.", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    application = QApplication(sys.argv)

    input_path = args.input
    if not input_path:
        input_path, _ = QFileDialog.getOpenFileName(None, "Open script", "", "Script (*.json)")
        if not input_path:
            sys.exit(0)

    try:
        script = Script.load(input_path)
    except (OSError, ValueError, KeyError) as error:
        sys.exit(f"Error: cannot read the script '{input_path}': {error}")
    window = ScriptViewerWindow(script, os.path.basename(input_path))
    window.showMaximized()
    sys.exit(application.exec_())
