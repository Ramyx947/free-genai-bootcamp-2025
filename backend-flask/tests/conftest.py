import pytest

from app import create_app
from app.extensions import db
from app.models import Group, Word


@pytest.fixture
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def sample_data(app):
    with app.app_context():
        word = Word(
            romanian="măr",
            english="apple",
            pronunciation="mur",
            part_of_speech="noun",
            parts=["fruit"],
        )
        db.session.add(word)

        group = Group(name="Test Group", description="Test Description", word_count=0)
        db.session.add(group)
        db.session.commit()


@pytest.fixture
def mock_openai(mocker):
    """Mock OpenAI API calls."""
    return mocker.patch("app.routes.vocabulary.generate_vocab_with_openai")
