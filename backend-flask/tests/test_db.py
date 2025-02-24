from app.extensions import db
from app.models import Word


def test_database(app):
    with app.app_context():
        # Create tables
        db.create_all()

        # Add test data
        word = Word(
            romanian="măr",
            english="apple",
            pronunciation="mur",
            part_of_speech="noun",
            parts=["fruit"],
        )
        db.session.add(word)
        db.session.commit()

        # Query and verify
        words = Word.query.all()
        assert len(words) > 0
        assert words[0].romanian == "măr"

        # Clean up
        db.drop_all()
