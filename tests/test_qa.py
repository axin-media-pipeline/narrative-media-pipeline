import tempfile
import unittest
import wave
from pathlib import Path
from src.qa import check

class QaTests(unittest.TestCase):
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(check([], Path(tmp)/"a.wav", [Path(tmp)/"missing"]))

    def test_duration_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp)/"a.wav"
            with wave.open(str(wav), "wb") as w:
                w.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
                w.writeframes(bytes(16000))
            self.assertTrue(check([{"start": 0, "end": 2}], wav, [wav]))
