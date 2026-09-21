#!/usr/bin/env python3
"""
Extract text from a text-based (non-scanned) PDF.

Install dependency:  pip install pypdf
Usage:               python3 extract_pdf.py textbook.pdf output.txt
"""

from argparse import ArgumentParser, Namespace

from pypdf import PdfReader

SCENE_REGEX = r"^\d+\.[[:space:]]Szene"

def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", help="The input pdf file which shall be converted.", type=str, required=True)
    parser.add_argument("--output", help="The output json file.", type=str, required=True)
    parser.add_argument("--startpage", help="The page to start at when parsing the document", type=int, default=1)
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

def parse_text(text: str) -> None:
    block_id = 0


if __name__ == "__main__":
    args = parse_arguments()
    text = extract(pdf_path=args.input, out_path=args.output, start_page=args.startpage)
    parse_text(text)