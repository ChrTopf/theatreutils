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


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The input pdf file which shall be converted.", type=str, required=True)
    parser.add_argument("--output", help="The output workbook file (.xlsx).", type=str, required=True)
    parser.add_argument("--startpage", help="The page to start at when parsing the document", type=int, default=1)
    parser.add_argument("--characters", help="The path to the characters.json file. The characters must be saved in a specific json structure.", type=str, required=True)
    return parser.parse_args()


def extract(pdf_path: str, out_path: str, start_page: int = 1) -> str:
    pages = []
    reader = PdfReader(pdf_path)
    with open(out_path, "w", encoding="utf-8") as out:
        for i, page in enumerate(reader.pages, start=1):
            if i >= start_page:
                text = page.extract_text() or ""
                pages.append(text + "\n")
    print(f"Done: {len(reader.pages)} pages -> {out_path}")
    return "".join(pages)


if __name__ == "__main__":
    args = parse_arguments()
    actors = Actor.load_list(args.characters)
    text = extract(pdf_path=args.input, out_path="out/parsed_text.txt", start_page=args.startpage)
    blocks = TextbookParser(actors).parse(text)
    WorkbookExporter().export(actors, blocks, args.output)
