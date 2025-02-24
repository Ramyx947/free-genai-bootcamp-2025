import json
from datetime import datetime

from ..extensions import db


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    romanian = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    pronunciation = db.Column(db.String(100))
    part_of_speech = db.Column(db.String(50))
    parts = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def from_db_row(row: tuple) -> "Word":
        return Word(
            id=row[0],
            romanian=row[1],
            english=row[2],
            pronunciation=row[3],
            part_of_speech=row[4],
            parts=json.loads(row[5]),
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7]),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "romanian": self.romanian,
            "english": self.english,
            "pronunciation": self.pronunciation,
            "part_of_speech": self.part_of_speech,
            "parts": self.parts,
        }


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    word_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def from_db_row(row: tuple) -> "Group":
        return Group(
            id=row[0],
            name=row[1],
            description=row[2],
            word_count=row[3],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5]),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "wordCount": self.word_count,
        }
