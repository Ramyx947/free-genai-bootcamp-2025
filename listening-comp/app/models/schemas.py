from pydantic import BaseModel
from typing import List, Optional

class VideoRequest(BaseModel):
    url: str

class Question(BaseModel):
    text: str
    options: List[str]
    correct_answer: int

class QuestionRequest(BaseModel):
    text: str
    num_questions: Optional[int] = 1
    difficulty: Optional[str] = "medium"

class QuestionResponse(BaseModel):
    status: str
    questions: List[Question]

class AudioResponse(BaseModel):
    audio_url: str
    duration: float = 0

class AudioRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None 