# Architecture

The public prototype uses a validated JSON script as input. The included example is original and does not reproduce the reference novel.

`script → TTS → optional RVC → measured timeline → audio assembly → master copy → illustration and video → QA → package`

- `src/script.py`: validate the script.
- `src/tts.py`: synthesize speech and decode to mono WAV.
- `voice/rvc_adapter.py` and `voice/rvc_worker.py`: interface with a separately installed RVC environment.
- `src/timeline.py`: schedule measured clips and generate SRT.
- `src/audio.py`: assemble clips into a narration track.
- `src/master_audio.py`: losslessly copy the master; normalization is not implemented yet.
- `src/visual.py`: generate a procedural still illustration.
- `src/qa.py`: check required files, timing order, and narration duration. It does not currently inspect video streams.
- `src/package.py`: bundle generated outputs.

This is a small reworking of a chapter-specific production workflow. The original chapter's authored scenes, text, assets, media, and project-specific production tools are outside the public repository.
