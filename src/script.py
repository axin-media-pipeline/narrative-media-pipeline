"""Load a structured script."""
import json
from pathlib import Path

def load_script(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    lines = data.get("lines")
    if not isinstance(lines, list) or not lines:
        raise ValueError("Script must contain a non-empty lines array")
    for line in lines:
        if not isinstance(line, dict) or not isinstance(line.get("text"), str) or not line["text"].strip():
            raise ValueError("Each line requires non-empty text")
        if not isinstance(line.get("speaker", "Narrator"), str):
            raise ValueError("Speaker must be a string")
    return data
