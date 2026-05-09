from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Segment(BaseModel):
    start: float
    end: float
    text: str


class TranscriptionResult(BaseModel):
    text: str
    segments: List[Segment]


class TranscriptionJob(BaseModel):
    id: str
    filename: str
    status: JobStatus
    result: Optional[TranscriptionResult] = None
    error: Optional[str] = None
