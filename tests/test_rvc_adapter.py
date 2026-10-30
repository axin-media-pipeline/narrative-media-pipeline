import shutil
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch
from voice.rvc_adapter import convert, _duration

class RvcTests(unittest.TestCase):
    def make_wav(self, path):
        with wave.open(str(path), "wb") as w:
            w.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
            w.writeframes(bytes(16000))

    def test_bypass_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/"a.wav", Path(tmp)/"b.wav"
            self.make_wav(source)
            self.assertEqual(convert(source, target), "bypassed")
            self.assertEqual(_duration(source), _duration(target))

    def test_mocked_rvc_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target = root/"a.wav", root/"b.wav"
            model, executable = root/"voice.pth", root/"python"
            self.make_wav(source)
            model.touch()
            executable.touch()
            def fake_run(args, check):
                shutil.copyfile(args[3], args[5])
            with patch("voice.rvc_adapter.subprocess.run", side_effect=fake_run):
                self.assertEqual(convert(source, target, model, executable, root), "converted")
            self.assertEqual(_duration(source), _duration(target))
