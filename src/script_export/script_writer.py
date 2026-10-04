import json
import os

from model.script import Script


class ScriptWriter:
    """Stores the Script for the script viewer as JSON file, overwriting an existing one."""

    def write(self, script: Script, output_path: str) -> None:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as script_file:
            json.dump(script.to_dict(), script_file, indent=4, ensure_ascii=False)
