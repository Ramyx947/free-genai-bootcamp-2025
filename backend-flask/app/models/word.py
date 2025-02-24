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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    groups = db.relationship('Group', 
                           secondary='word_groups',
                           backref=db.backref('words', lazy='dynamic')) 