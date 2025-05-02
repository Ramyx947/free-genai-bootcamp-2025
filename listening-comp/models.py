from pydantic import BaseModel
from typing import Dict, List, Optional

class VideoRequest(BaseModel):
    video_url: str

class Question(BaseModel):
    question: str
    options: Dict[str, str]
    correct_answer: str

class Dialogue(BaseModel):
    dialog: List[str]
    question: str
    options: Dict[str, str]
    correct_answer: str
    audio_path: Optional[str] = None

class DialogueResponse(BaseModel):
    dialogues: Dict[str, Dialogue]

class AudioResponse(BaseModel):
    audio_url: str
    duration: float 