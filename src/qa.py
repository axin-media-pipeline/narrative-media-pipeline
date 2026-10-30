"""Check files, narration bounds, and timeline agreement."""
from pathlib import Path
from .audio import duration

def check(timeline, audio_path, required, tolerance=0.05):
    errors = []
    for path in required:
        if not Path(path).is_file() or Path(path).stat().st_size == 0:
            errors.append(f"Missing or empty file: {Path(path).name}")
    previous_end = 0.0
    for line in timeline:
        if line["start"] < previous_end or line["end"] <= line["start"]:
            errors.append("Invalid or overlapping timeline")
        previous_end = line["end"]
    if timeline and Path(audio_path).is_file():
        if abs(duration(audio_path) - timeline[-1]["end"]) > tolerance:
            errors.append("Audio and timeline durations differ")
    return errors
