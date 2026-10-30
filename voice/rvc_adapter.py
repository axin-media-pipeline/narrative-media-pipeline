"""Thin subprocess adapter for an independently installed RVC implementation."""
from pathlib import Path
import shutil
import subprocess
import wave

def _duration(path):
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()

def convert(source, destination, model=None, backend=None, rvc_root=None, tolerance=0.001):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if model is None and backend is None and rvc_root is None:
        shutil.copyfile(source, destination)
        return "bypassed"
    if not all((model, backend, rvc_root)):
        raise ValueError("Model, RVC Python, and RVC root must be supplied together")
    model, backend, rvc_root = Path(model).resolve(), Path(backend).resolve(), Path(rvc_root).resolve()
    if not model.is_file() or not backend.is_file() or not rvc_root.is_dir():
        raise FileNotFoundError("Specified model, Python executable, or RVC root not found")
    worker = Path(__file__).with_name("rvc_worker.py")
    subprocess.run([str(backend), str(worker), str(rvc_root), str(source), str(model), str(destination)], check=True)
    if not destination.is_file() or abs(_duration(source) - _duration(destination)) > tolerance:
        destination.unlink(missing_ok=True)
        raise ValueError("Converted audio duration changed")
    return "converted"
