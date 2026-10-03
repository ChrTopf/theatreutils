import json
import os


class LispProjectWriter:
    """Stores a Linux Show Player project as `.lsp` (JSON) file, overwriting an existing one."""

    def write(self, project: dict, output_path: str) -> None:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as project_file:
            json.dump(project, project_file, indent=4, sort_keys=True, ensure_ascii=False)
