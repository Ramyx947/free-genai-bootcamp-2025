from unittest.mock import MagicMock, Mock, patch

import pytest

from app import create_app

# Patch the OpenAI client at module level to ensure it's patched before any imports
mock_client = MagicMock()
mock_client.chat.completions.create.return_value = MagicMock(
    choices=[MagicMock(message=MagicMock(content="Mocked response"))]
)


@pytest.fixture(autouse=True)
def patch_openai():
    """Patch OpenAI client for all tests in this module."""
    with patch("app.services.openai_service._client", mock_client):
        with patch(
            "app.services.openai_service.get_openai_client", return_value=mock_client
        ):
            yield


@pytest.fixture
def app():
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["GUARDRAILS_ENABLED"] = True

    # Mock database
    with patch("app.extensions.db") as mock_db:
        mock_db.init_app = Mock()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_vocabulary_endpoint_with_guardrails(app, client, monkeypatch):
    """Test that vocabulary endpoint works with guardrails enabled"""
    with app.app_context():
        # Create a simple dict result (JSON serializable)
        result = {"response": "Here is how to conjugate 'a merge'", "status": "success"}

        # Create a mock that returns our result
        async def mock_generate(*args, **kwargs):
            return result

        # Patch the async function
        monkeypatch.setattr(
            "app.services.openai_service.generate_vocabulary", mock_generate
        )

        # Patch the ChatOpenAI class
        with patch("app.utils.langchain_guardrails.ChatOpenAI"):
            # Also patch the LangChain guardrails methods
            with patch(
                "app.utils.langchain_guardrails.LangChainRomanianGuardrails.validate_input",
                return_value=True,
            ):
                with patch(
                    "app.utils.langchain_guardrails.LangChainRomanianGuardrails.process_output",
                    return_value=result["response"],
                ):
                    # Make the request
                    response = client.post(
                        "/api/vocabulary/generate",
                        json={
                            "text": "How do I conjugate 'a merge' in Romanian?",
                            "formal": True,
                            "prompt": "Teach me about verbs",
                        },
                    )

                    # Verify the response
                    assert response.status_code == 200
                    assert response.json["response"] == result["response"]
                    assert response.json["status"] == result["status"]


def test_guardrails_input_validation_failure(app, client):
    """Test that guardrails reject inappropriate input"""
    with app.app_context():
        # Patch the ChatOpenAI class
        with patch("app.utils.langchain_guardrails.ChatOpenAI"):
            # Patch the validate_input method to raise an error
            with patch(
                "app.utils.langchain_guardrails.LangChainRomanianGuardrails.validate_input",
                side_effect=ValueError("Input contains inappropriate content"),
            ):
                # Make the request with "bad" input
                response = client.post(
                    "/api/vocabulary/generate",
                    json={
                        "text": "Some inappropriate text",
                        "formal": True,
                        "prompt": "Teach me about verbs",
                    },
                )

                # Verify the response indicates an error
                assert response.status_code == 400
                assert "inappropriate content" in response.json["error"].lower()


def test_guardrails_output_processing(app, client, monkeypatch):
    """Test that guardrails properly process the output"""
    with app.app_context():
        # Create a result with informal text
        result = {"response": "tu esti student", "status": "success"}

        # Create a mock that returns our result
        async def mock_generate(*args, **kwargs):
            return result

        # Patch the async function
        monkeypatch.setattr(
            "app.services.openai_service.generate_vocabulary", mock_generate
        )

        # Patch the ChatOpenAI class
        with patch("app.utils.langchain_guardrails.ChatOpenAI"):
            # Patch the validate_input and process_output methods
            with patch(
                "app.utils.langchain_guardrails.LangChainRomanianGuardrails.validate_input",
                return_value=True,
            ):
                # Configure the process_output mock to return formal text for formal=True
                with patch(
                    "app.utils.langchain_guardrails.LangChainRomanianGuardrails.process_output"
                ) as mock_process:

                    def side_effect(text, formal):
                        if formal:
                            return "dumneavoastră sunteți student"
                        else:
                            return "tu esti student"

                    mock_process.side_effect = side_effect

                    # Make the request with formal=True
                    response = client.post(
                        "/api/vocabulary/generate",
                        json={
                            "text": "How do I say 'you are a student' in Romanian?",
                            "formal": True,
                            "prompt": "Teach me formal speech",
                        },
                    )

                    # Verify the response has been processed to formal
                    assert response.status_code == 200
                    assert "dumneavoastră sunteți" in response.json["response"].lower()

                    # Now test with formal=False
                    response = client.post(
                        "/api/vocabulary/generate",
                        json={
                            "text": "How do I say 'you are a student' in Romanian?",
                            "formal": False,
                            "prompt": "Teach me informal speech",
                        },
                    )

                    # Verify the response is informal
                    assert response.status_code == 200
                    assert "tu esti" in response.json["response"].lower()
