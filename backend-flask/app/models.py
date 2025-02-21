from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

@dataclass
class Word:
    id: int
    romanian: str
    english: str
    pronunciation: str
    part_of_speech: str
    parts: List[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_db_row(row: tuple) -> 'Word':
        return Word(
            id=row[0],
            romanian=row[1],
            english=row[2],
            pronunciation=row[3],
            part_of_speech=row[4],
            parts=json.loads(row[5]),  # Convert JSON string to list
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7])
        )

@dataclass
class Group:
    id: int
    name: str
    description: Optional[str]
    word_count: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_db_row(row: tuple) -> 'Group':
        return Group(
            id=row[0],
            name=row[1],
            description=row[2],
            word_count=row[3],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5])
        )

@dataclass
class WordGroup:
    id: int
    word_id: int
    group_id: int

    @staticmethod
    def from_db_row(row: tuple) -> 'WordGroup':
        return WordGroup(
            id=row[0],
            word_id=row[1],
            group_id=row[2]
        )

@dataclass
class StudySession:
    id: int
    activity_id: str
    group_id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    score: float

    @staticmethod
    def from_db_row(row: tuple) -> 'StudySession':
        return StudySession(
            id=row[0],
            activity_id=row[1],
            group_id=row[2],
            start_time=datetime.fromisoformat(row[3]),
            end_time=datetime.fromisoformat(row[4]) if row[4] else None,
            score=row[5]
        )

@dataclass
class StudyActivity:
    id: str
    type: str  # 'vocabulary', 'reading', or 'grammar'
    title: str
    description: Optional[str]
    thumbnail_url: Optional[str]
    progress: float
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_db_row(row: tuple) -> 'StudyActivity':
        return StudyActivity(
            id=row[0],
            type=row[1],
            title=row[2],
            description=row[3],
            thumbnail_url=row[4],
            progress=row[5],
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7])
        )

@dataclass
class WordReviewItem:
    id: int
    word_id: int
    session_id: int
    correct: bool
    user_answer: str
    correct_answer: str
    created_at: datetime

    @staticmethod
    def from_db_row(row: tuple) -> 'WordReviewItem':
        return WordReviewItem(
            id=row[0],
            word_id=row[1],
            session_id=row[2],
            correct=bool(row[3]),
            user_answer=row[4],
            correct_answer=row[5],
            created_at=datetime.fromisoformat(row[6])
        )
