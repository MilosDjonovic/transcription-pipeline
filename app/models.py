from pydantic import BaseModel
from typing import List


class Segment(BaseModel):
    start: float
    end: float
    text: str


class TranscriptResponse(BaseModel):
    text: str
    segments: List[Segment]