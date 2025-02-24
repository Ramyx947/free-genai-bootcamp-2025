from ..extensions import db

class WordGroup(db.Model):
    __tablename__ = "word_groups"
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True) 