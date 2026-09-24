#!/usr/bin/env python3
"""
Extract text from a text-based (non-scanned) PDF and parse it into a
structured theatre dataset (characters + blocks), exportable as JSON.

Install dependency:  pip install pypdf
Usage:               python3 pdftojson.py --input textbook.pdf --output out.json --characters characters.json
"""

from argparse import ArgumentParser, Namespace
from pypdf import PdfReader

from actor import Actor
from textbook_parser import TextbookParser
from workbook_exporter import WorkbookExporter
from page import Page


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The input pdf file which shall be converted.", type=str, required=True)
    parser.add_argument("--output", help="The output workbook file (.xlsx).", type=str, required=True)
    parser.add_argument("--startpage", help="The page to start at when parsing the document", type=int, default=1)
    parser.add_argument("--characters", help="The path to the characters.json file. The characters must be saved in a specific json structure.", type=str, required=True)
    parser.add_argument("--trim-first-line", help="Specify if the first line of every page should be removed.", action='store_true')
    parser.add_argument("--trim-last-line", help="Specify, if the last line of every page should be removed.", action='store_true')
    return parser.parse_args()


def extract_pages(pdf_path: str, start_page: int = 1) -> list[Page]:
    pages = []
    reader = PdfReader(pdf_path)
    for i, page in enumerate(reader.pages, start=1):
        if i >= start_page:
            pages.append(Page(page.extract_text() or "", i))
    return pages

def trim_first_line(pages: list[Page]) -> None:
    for page in pages:
        page.text = "\n".join(page.text.split("\n")[1:])

def trim_last_line(pages: list[Page]) -> None:
    for page in pages:
        page.text = "\n".join(page.text.split("\n")[:-1])

if __name__ == "__main__":
    args = parse_arguments()
    actors = Actor.load_list(args.characters)
    pages = extract_pages(pdf_path=args.input, start_page=args.startpage)
    if args.trim_first_line:
        trim_first_line(pages)
    if args.trim_last_line:
        trim_last_line(pages)
    blocks = TextbookParser(actors).parse(pages)
    WorkbookExporter().export(actors, blocks, args.output)
