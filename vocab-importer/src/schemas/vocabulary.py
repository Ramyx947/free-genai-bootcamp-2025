from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Word(BaseModel):
    word: str = Field(..., min_length=1, max_length=100)
    translation: Optional[str] = Field(None, max_length=100)
    context: Optional[str] = Field(None, max_length=500)

class VocabularyGroup(BaseModel):
    group: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    words: List[Word]

    @validator('words')
    def validate_words(cls, v):
        if not v:
            raise ValueError('Group must contain at least one word')
        return v

class VocabularyImport(BaseModel):
    groups: List[VocabularyGroup] 