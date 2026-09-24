#!/usr/bin/env python3
"""
Extract text from a text-based (non-scanned) PDF.

Install dependency:  pip install pypdf
Usage:               python3 extract_pdf.py textbook.pdf output.txt
"""

from argparse import ArgumentParser, Namespace
import json
from pypdf import PdfReader

SCENE_REGEX = r"^\d+\.[[:space:]]Szene"
OPENING_REGEX = r"^Vorspann"
ACT_REGEX = r"^\d+\.[[:space:]]Akt"

def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The input pdf file which shall be converted.", type=str, required=True)
    parser.add_argument("--output", help="The output json file.", type=str, required=True)
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

def parse_text(text: str, characters: list[object]) -> None:
    block_id = 0


def parse_characters(characters_path: str) -> list[object]:
    with open(characters_path, "r", encoding="utf-8") as char_file:
        return json.load(char_file)

if __name__ == "__main__":
    args = parse_arguments()
    characters = parse_characters(characters_path=args.characters)
    text = extract(pdf_path=args.input, out_path=args.output, start_page=args.startpage)
    with open("out/parsed_text.txt", "w", encoding="utf-8") as out:
        out.write(text)
    parse_text(text, characters)