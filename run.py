"""Generate a narrated audiovisual demo from a structured script."""
import argparse
import json
from pathlib import Path
import subprocess

from src import audio, master_audio, qa, script, timeline, tts, visual
from src.package import package
from voice.rvc_adapter import convert

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--script", default="examples/sample_script.json")
    p.add_argument("--output", default="output")
    p.add_argument("--ffmpeg", default="ffmpeg")
    p.add_argument("--voice", default="en-US-AriaNeural")
    p.add_argument("--rvc-model")
    p.add_argument("--rvc-python")
    p.add_argument("--rvc-root")
    args = p.parse_args()
    if any((args.rvc_model, args.rvc_python, args.rvc_root)) and not all((args.rvc_model, args.rvc_python, args.rvc_root)):
        p.error("--rvc-model, --rvc-python, and --rvc-root must be supplied together")
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    temp = out / "clips"
    temp.mkdir(exist_ok=True)
    data = script.load_script(args.script)
    clips = []
    for i, line in enumerate(data["lines"]):
        source = temp / f"source-{i:03}.wav"
        final = temp / f"line-{i:03}.wav"
        tts.synthesize(line["text"], args.voice, source, args.ffmpeg)
        mode = convert(source, final, args.rvc_model, args.rvc_python, args.rvc_root)
        print(f"Line {i + 1}: {mode}")
        clips.append(final)
    timings = timeline.build_timeline(data["lines"], [audio.duration(p) for p in clips])
    subs = out / "subtitles.srt"
    subs.write_text(timeline.subtitles(timings), encoding="utf-8")
    timings_file = out / "timeline.json"
    timings_file.write_text(json.dumps(timings, ensure_ascii=False, indent=2), encoding="utf-8")
    premaster = temp / "premaster.wav"
    audio.assemble(clips, timings, premaster)
    master = out / "narration.wav"
    master_audio.master(premaster, master)
    image = temp / "scene.ppm"
    visual.create(image)
    video = out / "demo.mp4"
    subprocess.run([args.ffmpeg, "-v", "error", "-y", "-loop", "1", "-framerate", "24",
        "-i", str(image),
        "-i", str(master), "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", str(video)], check=True)
    errors = qa.check(timings, master, [subs, video, timings_file])
    if errors:
        raise RuntimeError("; ".join(errors))
    bundle = out / "deliverables.zip"
    package([master, subs, timings_file, video], bundle)
    print(f"Done: {bundle}")

if __name__ == "__main__":
    main()
