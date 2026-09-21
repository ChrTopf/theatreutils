#!/usr/bin/env python3
"""
Extract text from a text-based (non-scanned) PDF.

Install dependency:  pip install pypdf
Usage:               python3 extract_pdf.py textbook.pdf output.txt
"""

import sys
from pypdf import PdfReader


def extract(pdf_path: str, out_path: str) -> None:
    reader = PdfReader(pdf_path)
    with open(out_path, "w", encoding="utf-8") as out:
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            out.write(f"\n===== PAGE {i} =====\n")
            out.write(text.strip() + "\n")
    print(f"Done: {len(reader.pages)} pages -> {out_path}")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "textbook.pdf"
    out = sys.argv[2] if len(sys.argv) > 2 else "out/output.txt"
    extract(pdf, out)