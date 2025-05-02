from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    text: str
    options: List[str]
    correct_answer: int
    difficulty: Optional[float] = None

class QuestionRequest(BaseModel):
    text: str
    num_questions: Optional[int] = 1
    difficulty: Optional[str] = "medium"

class QuestionResponse(BaseModel):
    status: str
    questions: List[Question]
