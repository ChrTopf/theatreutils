from dataclasses import dataclass

from page import Page


@dataclass(frozen=True)
class Line:
    """A single, whitespace-trimmed line of the textbook together with the page it was found on."""

    text: str
    page_number: int

    @property
    def is_blank(self) -> bool:
        return not self.text


def lines_from_pages(pages: list[Page]) -> list[Line]:
    """Flattens the pages into one continuous list of lines.

    Pages are concatenated without a separator so that dialogue and paragraphs
    spanning a page break are still recognized as a single block.
    """
    return [
        Line(text=raw_line.strip(), page_number=page.number)
        for page in pages
        for raw_line in page.text.splitlines()
    ]
