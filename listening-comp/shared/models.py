from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class DialogueEntry(BaseModel):
    speaker: str
    text: str
    timestamp: Optional[float] = None

class Dialogue(BaseModel):
    dialog: List[str]
    question: str
    options: Dict[str, str]
    correct_answer: str
    audio_path: Optional[str] = None
    created_at: datetime = datetime.now()

class AudioRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    language_code: str = "ro-RO"

class AudioResponse(BaseModel):
    audio_data: str
    duration: float
    format: str = "mp3" 