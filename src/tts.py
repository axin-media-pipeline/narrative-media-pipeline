"""Synthesize narration using edge-tts and decode with FFmpeg."""
import asyncio
import subprocess

async def _synthesize(text, voice, path):
    import edge_tts
    await edge_tts.Communicate(text, voice).save(str(path))

def synthesize(text, voice, target, ffmpeg):
    mp3 = target.with_suffix(".mp3")
    asyncio.run(_synthesize(text, voice, mp3))
    subprocess.run([ffmpeg, "-v", "error", "-y", "-i", str(mp3), "-ar", "48000",
                    "-ac", "1", "-c:a", "pcm_s16le", str(target)], check=True)
    mp3.unlink()
