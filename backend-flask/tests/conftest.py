import pytest

from app import create_app
from app.extensions import db
from app.models import Group, Word


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    with app.app_context():
        db.create_all()  # Create tables before tests
        yield app
        db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def sample_data(app):
    """Create sample data for tests."""
    with app.app_context():
        # Create tables
        db.create_all()

        # Add sample word
        word = Word(
            romanian="măr",
            english="apple",
            pronunciation="mur",
            part_of_speech="noun",
            parts=["fruit"],
        )

        # Add sample group
        group = Group(
            name="Fruits", description="Romanian fruit vocabulary", word_count=1
        )

        db.session.add(word)
        db.session.add(group)
        db.session.commit()

        yield  # This allows the test to run

        # Cleanup
        db.session.remove()
        db.drop_all()


@pytest.fixture
def mock_openai(mocker):
    """Mock OpenAI API calls."""
    return mocker.patch("app.routes.vocabulary.generate_vocab_with_openai")
