#!/usr/bin/env python3
"""
Display the blocks of a workbook produced by script_parser.py (optionally enriched
with audio and light effects) to follow the text during the live show.

Install dependency:  pip install pyqt5 openpyxl
Usage:               python3 script_viewer.py --input blocks.xlsx

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

from script_viewer_ui import ScriptViewerWindow
from workbook_importer import WorkbookImporter


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The workbook file (.xlsx) to display. A file dialog is shown if omitted.", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    application = QApplication(sys.argv)

    input_path = args.input
    if not input_path:
        input_path, _ = QFileDialog.getOpenFileName(None, "Open workbook", "", "Excel workbook (*.xlsx)")
        if not input_path:
            sys.exit(0)

    blocks = WorkbookImporter().import_blocks(input_path)
    window = ScriptViewerWindow(blocks, os.path.basename(input_path))
    window.showMaximized()
    sys.exit(application.exec_())
