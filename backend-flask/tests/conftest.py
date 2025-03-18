"""Test fixtures for the Flask application."""

import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.models import Group, Word
from app.utils.guardrails import GuardrailResult

# Create a global mock for OpenAI client
mock_openai_client = MagicMock()
mock_openai_client.chat.completions.create.return_value = MagicMock(
    choices=[MagicMock(message=MagicMock(content="Mocked response"))]
)


@pytest.fixture(autouse=True)
def patch_openai() -> Generator[None, None, None]:
    """Patch OpenAI client for all tests."""
    with patch("app.services.openai_service._client", mock_openai_client):
        with patch(
            "app.services.openai_service.get_openai_client",
            return_value=mock_openai_client,
        ):
            yield


@pytest.fixture(autouse=True)
def mock_openai() -> Generator[None, None, None]:
    """Mock OpenAI API calls for all tests."""
    with patch("langchain_openai.ChatOpenAI"):
        with patch("app.utils.langchain_guardrails.ChatOpenAI"):
            yield


@pytest.fixture(autouse=True)
def mock_guardrails() -> Generator[None, None, None]:
    """Mock guardrails for all tests."""
    with patch(
        "app.utils.guardrails.RomanianGuardrails.validate_input",
        return_value=GuardrailResult(True, filtered_content="Test input"),
    ):
        with patch(
            "app.utils.guardrails.RomanianGuardrails.process_output",
            return_value=GuardrailResult(True, filtered_content="Test output"),
        ):
            yield


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create and configure a Flask application for testing.

    Returns:
        Flask: Configured Flask application for testing
    """
    app = create_app("testing")

    # Create the database and tables
    with app.app_context():
        db.create_all()

        # Create some test data
        group = Group(name="Fruits", description="Romanian fruit vocabulary")
        db.session.add(group)

        word = Word(
            romanian="măr", english="apple", part_of_speech="noun", parts=["fruit"]
        )
        db.session.add(word)

        db.session.commit()

        yield app

        # Clean up
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the app.

    Args:
        app: Flask application

    Returns:
        FlaskClient: Test client for making requests
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
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
def mock_openai_for_routes(mocker):
    """Mock OpenAI API calls for routes."""
    return mocker.patch("app.routes.vocabulary.generate_vocab_with_openai")


@pytest.fixture
def test_word(app):
    """Create a test word in the database."""
    with app.app_context():
        word = Word(
            romanian="casă", english="house", part_of_speech="noun", parts=["building"]
        )
        db.session.add(word)
        db.session.commit()
        yield word
        db.session.delete(word)
        db.session.commit()


@pytest.fixture
def test_group(app):
    """Create a test group in the database."""
    with app.app_context():
        group = Group(name="Test Group", description="A test group")
        db.session.add(group)
        db.session.commit()
        yield group
        db.session.delete(group)
        db.session.commit()


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    with patch("app.services.openai_service.generate_vocabulary") as mock:
        mock.return_value = {
            "status": "success",
            "response": "This is a test response",
            "cached": False,
        }
        yield mock


def create_word(**kwargs):
    # Map 'text' to 'romanian' if present
    if "text" in kwargs:
        kwargs["romanian"] = kwargs.pop("text")
    # Map 'translation' to 'english' if present
    if "translation" in kwargs:
        kwargs["english"] = kwargs.pop("translation")
    # Remove 'example' if present
    if "example" in kwargs:
        kwargs.pop("example")
    # Ensure 'parts' is present
    if "parts" not in kwargs:
        kwargs["parts"] = []
    return Word(**kwargs)


@pytest.fixture
def sample_word():
    return create_word(
        text="măr",
        translation="apple",
        part_of_speech="noun",
        example="Mărul este roșu.",
    )
