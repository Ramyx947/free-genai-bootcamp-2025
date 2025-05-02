from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class TranscriptSegment:
    text: str
    start_time: float
    end_time: float
    duration: float
    speaker_id: Optional[str] = None
    confidence: float = 1.0

@dataclass
class TranscriptMetadata:
    video_id: str
    title: str
    language: str = "ro"
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    upload_date: Optional[str] = None
    duration: Optional[float] = None
    processed_date: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class TranscriptData:
    metadata: TranscriptMetadata
    segments: List[TranscriptSegment]
    raw_transcript: str
    
    def to_dict(self) -> Dict:
        return {
            "metadata": {
                "video_id": self.metadata.video_id,
                "title": self.metadata.title,
                "language": self.metadata.language,
                "channel_id": self.metadata.channel_id,
                "channel_name": self.metadata.channel_name,
                "upload_date": self.metadata.upload_date,
                "duration": self.metadata.duration,
                "processed_date": self.metadata.processed_date
            },
            "segments": [
                {
                    "text": seg.text,
                    "start_time": seg.start_time,
                    "end_time": seg.end_time,
                    "duration": seg.duration,
                    "speaker_id": seg.speaker_id,
                    "confidence": seg.confidence
                }
                for seg in self.segments
            ],
            "raw_transcript": self.raw_transcript
        } 