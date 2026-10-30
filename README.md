# narrative-media-pipeline

A small, script-driven media production pipeline developed from the workflow used in a longer narrative adaptation. It turns a structured script into synthesized narration, a measured timeline, editable subtitles, a simple illustrated video, and a deliverable archive. The public sample is an original, two-line story.

This repository is an early, deliberately small extraction, not the complete chapter production system. Its current video is a still illustration with narration; it does not yet animate scenes or burn subtitles into the picture.

## How it works

1. Load and validate a JSON script.
2. Generate narration with Edge TTS, optionally apply an independently installed RVC voice conversion.
3. Measure the resulting WAV clips, construct a timeline, and generate SRT subtitles.
4. Assemble lossless narration, create a procedural illustration and encode an MP4 with FFmpeg.
5. Check required files and audio/timeline duration, then create a ZIP.

Audio is generated before the final timeline because actual synthesized durations are needed for synchronization. The current mastering step copies the WAV; loudness normalization is planned.

## Quickstart

Requires Python 3.11, FFmpeg on PATH, and internet access for Edge TTS.

```sh
python -m pip install -r requirements.txt
python run.py --script examples/sample_script.json --output output
```

The demo writes `output/narration.wav`, `output/subtitles.srt`, `output/timeline.json`, `output/demo.mp4` and `output/deliverables.zip`. For a non-default FFmpeg location, pass `--ffmpeg /path/to/ffmpeg`. The video contains a still image and audio; subtitles are delivered as a separate SRT file.

### Optional RVC conversion

Without RVC options, original TTS audio is used. With a separately installed compatible RVC environment and an authorized model, add:

```sh
python run.py --script examples/sample_script.json --output output \
  --rvc-root /path/to/rvc \
  --rvc-python /path/to/rvc/python \
  --rvc-model /path/to/authorized-model.pth
```

The external RVC environment supplies its own dependencies and support models. The adapter calls its Python interface; compatibility with every fork or version is not guaranteed. Converted clips are resampled to 48 kHz and small differences of at most 100 ms are trimmed or padded to preserve timing. A larger discrepancy fails. Models are never included in this repository. Use only voices you have permission to use.

## Demonstration

- [Original sample script](examples/sample_script.json)
- [Sample illustration](examples/sample_output/scene.png)
- [Architecture](docs/ARCHITECTURE.md)

## Technology

Python, Edge TTS, FFmpeg, GitHub Actions, and optionally an external RVC environment. Tests use Python's standard library.

```sh
python -m unittest discover -s tests -v
```

## Roadmap and potential Devin tasks

- Extend tests for timeline edge cases, generated media and conversion failures.
- Check actual video and audio duration and report synchronization drift.
- Replace the still-image demo with configurable scene and shot rendering.
- Implement audio loudness normalization and separate mixing tracks.
- Add retry and recovery for speech synthesis and rendering failures.
- Improve RVC integration across compatible installations and validate model provenance.
- Make output packaging deterministic and validate archive contents.
- Expand CI across operating systems and publish artifacts from reviewed pull requests.

## Third-party

RVC is an optional voice conversion module maintained by [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) under its own MIT license. It is not included here, and this project does not claim authorship of RVC. Edge TTS, FFmpeg and other external components have their own licenses and service terms. No voice models are distributed here.

## License

Project-owned code is available under the MIT License; see [LICENSE](LICENSE). Third-party software, models, services, and source material have their own terms. See [NOTICE](NOTICE).
