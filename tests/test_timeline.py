import unittest
from src.timeline import build_timeline, subtitles, timestamp

class TimelineTests(unittest.TestCase):
    def test_gap_and_duration(self):
        result = build_timeline([{"text": "A"}, {"text": "B"}], [1.25, 2.0])
        self.assertAlmostEqual(result[1]["start"], 1.6)
        self.assertAlmostEqual(result[1]["end"], 3.6)

    def test_srt_format(self):
        self.assertEqual(timestamp(61.25), "00:01:01,250")
        self.assertIn("00:00:00,000 --> 00:00:01,000",
            subtitles(build_timeline([{"text": "A"}], [1])))

    def test_reject_missing_duration(self):
        with self.assertRaises(ValueError):
            build_timeline([{"text": "A"}], [])
