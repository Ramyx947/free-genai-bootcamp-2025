from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, validator


class Word(BaseModel):
    word: str = Field(..., min_length=1, max_length=100)
    translation: Optional[str] = Field(None, max_length=100)
    context: Optional[str] = Field(None, max_length=500)


class VocabularyGroup(BaseModel):
    group: str
    words: list[str]

    @field_validator("words")
    def validate_words(cls, v):
        if not v:
            raise ValueError("Words list cannot be empty")
        return v


class VocabularyImport(BaseModel):
    groups: List[VocabularyGroup]
