"""Assemble WAV clips at positions defined by the timeline."""
import wave

def duration(path):
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()

def assemble(clips, timeline, target):
    chunks = []
    position = 0
    rate = 48000
    for path, line in zip(clips, timeline):
        with wave.open(str(path), "rb") as wav:
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (1, 2, rate):
                raise ValueError(f"Unexpected WAV format: {path}")
            data = wav.readframes(wav.getnframes())
        start = round(line["start"] * rate)
        if start < position:
            raise ValueError("Overlapping narration clips")
        chunks.append(b"\0\0" * (start - position))
        chunks.append(data)
        position = start + len(data) // 2
    with wave.open(str(target), "wb") as wav:
        wav.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        for chunk in chunks:
            wav.writeframes(chunk)
