import os
import uuid
from typing import Dict

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse

from app.utils import validate_audio_file, convert_to_wav
from app.transcriber import transcribe_audio
from app.models import TranscriptionJob, JobStatus, TranscriptionResult


app = FastAPI(
    title="Transcription Pipeline",
    description="A simple transcription pipeline using OpenAI Whisper and FastAPI."
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mock database to store job statuses
jobs: Dict[str, TranscriptionJob] = {}


def run_transcription_task(job_id: str, original_path: str):
    job = jobs[job_id]
    job.status = JobStatus.PROCESSING
    print(f"[*] Starting transcription for job: {job_id}")
    
    wav_path = os.path.join(UPLOAD_DIR, f"{job_id}.wav")
    
    try:
        # Convert to WAV (mono, 16kHz as per Whisper best practices)
        convert_to_wav(original_path, wav_path)
        
        # Transcribe
        result_data = transcribe_audio(wav_path)
        
        # Update job with result
        job.result = TranscriptionResult(**result_data)
        job.status = JobStatus.COMPLETED
        print(f"[+] Job {job_id} completed successfully.")
        
    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)
        print(f"[-] Job {job_id} failed: {e}")
    finally:
        # Cleanup files
        if os.path.exists(original_path):
            os.remove(original_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)


@app.post("/transcribe", response_model=TranscriptionJob)
async def transcribe(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        validate_audio_file(file.filename, file.content_type)
        
        job_id = str(uuid.uuid4())
        original_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
        
        # Save uploaded file
        with open(original_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # Create job entry
        job = TranscriptionJob(
            id=job_id,
            filename=file.filename,
            status=JobStatus.PENDING
        )
        jobs[job_id] = job
        
        # Add task to background
        background_tasks.add_task(run_transcription_task, job_id, original_path)
        
        return job

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in /transcribe: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/status/{job_id}", response_model=TranscriptionJob)
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]


@app.get("/status/{job_id}/text", response_class=PlainTextResponse)
async def get_status_text(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs[job_id]
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Job status is {job.status}")
    return job.result.text


@app.get("/jobs")
async def list_jobs():
    return list(jobs.values())
