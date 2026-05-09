import whisper

model = whisper.load_model("small")


def transcribe_audio(file_path: str):
    result = model.transcribe(
        file_path,
        language="en"
    )

    segments = []

    for seg in result["segments"]:
        segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip()
        })

    return {
        "text": result["text"].strip(),
        "segments": segments
    }