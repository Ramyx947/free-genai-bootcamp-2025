"""
Word Model

Represents a vocabulary word in the Romanian learning system.
Each word has:
- Romanian and English translations
- Pronunciation guide
- Part of speech
- Learning status
- Group associations
"""

from datetime import datetime

from ..extensions import db


class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    romanian = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    pronunciation = db.Column(db.String(100))
    part_of_speech = db.Column(db.String(50), nullable=False)
    parts = db.Column(db.JSON, nullable=False)
    learned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    groups = db.relationship(
        "Group", secondary="word_groups", backref=db.backref("words", lazy="dynamic")
    )

    def to_dict(self):
        """Convert Word model to dictionary.

        Returns:
            dict: Word data in format matching API specs
        """
        return {
            "id": self.id,
            "romanian": self.romanian,
            "english": self.english,
            "pronunciation": self.pronunciation,
            "part_of_speech": self.part_of_speech,
            "parts": self.parts,
            "learned": self.learned,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "groupIds": [g.id for g in self.groups],
        }
