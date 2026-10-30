"""Build a timeline from measured narration durations."""
def build_timeline(lines, durations, gap=0.35):
    if len(lines) != len(durations) or gap < 0:
        raise ValueError("Invalid duration list or gap")
    time = 0.0
    result = []
    for line, duration in zip(lines, durations):
        if duration <= 0:
            raise ValueError("Duration must be positive")
        start = time
        end = start + duration
        result.append({"speaker": line.get("speaker", "Narrator"),
                       "text": line["text"], "start": start, "end": end})
        time = end + gap
    return result

def timestamp(seconds):
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{hours:02}:{minutes:02}:{sec:02},{ms:03}"

def subtitles(timeline):
    return "\n".join(
        f"{i}\n{timestamp(line['start'])} --> {timestamp(line['end'])}\n{line['text']}\n"
        for i, line in enumerate(timeline, 1)
    )
