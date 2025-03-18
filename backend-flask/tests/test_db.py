"""Database functionality tests.

Tests core database operations:
- Creating and retrieving models
- Relationships between models
- Query functionality
"""

from app import db
from app.models import Group, Word


def test_database(app) -> None:
    """Test basic database CRUD operations and relationships."""
    with app.app_context():
        # Test creating a new word
        word = Word(
            romanian="casă", english="house", part_of_speech="noun", parts=["building"]
        )
        db.session.add(word)
        db.session.commit()

        # Test retrieving the word
        retrieved_word = Word.query.filter_by(romanian="casă").first()
        assert retrieved_word is not None
        assert retrieved_word.english == "house"

        # Test creating a new group
        group = Group(name="Basic Vocabulary", description="Essential Romanian words")
        db.session.add(group)
        db.session.commit()

        # Test retrieving the group
        retrieved_group = Group.query.filter_by(name="Basic Vocabulary").first()
        assert retrieved_group is not None
        assert retrieved_group.description == "Essential Romanian words"

        # Test adding a word to a group
        retrieved_group.words.append(retrieved_word)
        db.session.commit()

        # Test retrieving words in a group
        assert retrieved_group.words.count() == 1
        assert retrieved_group.words[0].romanian == "casă"
