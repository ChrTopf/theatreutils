import os

from snippet_export.x32_snippet import X32Snippet

FIRST_SNIPPET_NUMBER = 1


class SnippetWriter:
    """Stores snippets as `<theater-name>.<3-digit-number>.snp` files, numbered from 001 in play order.

    This naming scheme is the one used by the X32-Edit application. Existing
    files with the same names are overwritten.
    """

    def write(self, snippets: list[X32Snippet], output_dir: str, theater_name: str) -> list[str]:
        os.makedirs(output_dir, exist_ok=True)
        paths = []
        for number, snippet in enumerate(snippets, start=FIRST_SNIPPET_NUMBER):
            path = os.path.join(output_dir, f"{theater_name}.{number:03d}.snp")
            # The console only knows ASCII characters, anything else becomes a "?".
            with open(path, "w", encoding="ascii", errors="replace", newline="\n") as snippet_file:
                snippet_file.write(snippet.to_text())
            paths.append(path)
        return paths
