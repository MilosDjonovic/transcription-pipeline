import os
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException

from app.utils import validate_audio_file, convert_to_wav
from app.transcriber import transcribe_audio


app = FastAPI(title="Transcription Pipeline")


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        validate_audio_file(file.filename)

        file_id = str(uuid.uuid4())

        original_path = os.path.join(
            UPLOAD_DIR,
            f"{file_id}_{file.filename}"
        )

        with open(original_path, "wb") as f:
            content = await file.read()
            f.write(content)

        wav_path = os.path.join(
            UPLOAD_DIR,
            f"{file_id}.wav"
        )

        convert_to_wav(original_path, wav_path)

        result = transcribe_audio(wav_path)

        return {
            "success": True,
            "filename": file.filename,
            "transcript": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))