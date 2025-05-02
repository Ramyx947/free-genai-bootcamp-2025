from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TranscriptSegment(BaseModel):
    text: str
    start_time: float
    end_time: float
    duration: float

class TranscriptMetadata(BaseModel):
    video_id: str
    title: str
    channel_id: Optional[str]
    channel_name: Optional[str]
    upload_date: Optional[str]
    duration: Optional[int]

class TranscriptData(BaseModel):
    metadata: TranscriptMetadata
    segments: List[TranscriptSegment]
    raw_transcript: str
