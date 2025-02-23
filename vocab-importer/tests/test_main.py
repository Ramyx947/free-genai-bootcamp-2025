import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from vocab_importer.main import generate_vocab_with_openai
from vocab_importer.src.main import create_app


def test_generate_vocab_with_openai_development_mode():
    with patch.dict("os.environ", {"DEVELOPMENT_MODE": "true"}):
        result = generate_vocab_with_openai()
        assert "groups" in result
        assert len(result["groups"]) == 2
        assert result["groups"][0]["group"] == "Basic Greetings"


@patch("vocab_importer.main.client.chat.completions.create")
def test_generate_vocab_with_openai_api_call(mock_create):
    # Create mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content=(
                    '{"groups": [{"group": "Test Group", '
                    '"words": ["test1", "test2"]}]}'
                )
            )
        )
    ]
    mock_create.return_value = mock_response

    result = generate_vocab_with_openai()

    # Verify API call
    mock_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that generates vocabulary groups.",
            },
            {
                "role": "user",
                "content": (
                    "Generate a list of vocabulary groups for a language learning app. "
                    "Each group should have a 'group' key and a 'words' key which is "
                    "a list of words. Return the output in valid JSON format."
                ),
            },
        ],
        temperature=0.7,
        max_tokens=300,
    )

    # Verify result
    assert "groups" in result
    assert len(result["groups"]) == 1
    assert result["groups"][0]["group"] == "Test Group"


@patch("vocab_importer.main.client.chat.completions.create")
def test_generate_vocab_with_openai_error_handling(mock_create):
    mock_create.side_effect = Exception("API Error")

    result = generate_vocab_with_openai()
    assert "error" in result
    assert "API Error" in result["error"]


@patch("vocab_importer.main.client.chat.completions.create")
def test_generate_vocab_with_custom_prompt(mock_create):
    custom_prompt = "Generate vocabulary for animals"

    # Create mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content='{"groups": [{"group": "Animals", "words": ["cat", "dog"]}]}'
            )
        )
    ]
    mock_create.return_value = mock_response

    result = generate_vocab_with_openai(prompt=custom_prompt)

    # Verify API call
    mock_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that generates vocabulary groups.",
            },
            {"role": "user", "content": custom_prompt},
        ],
        temperature=0.7,
        max_tokens=300,
    )

    assert "groups" in result
    assert result["groups"][0]["group"] == "Animals"


@patch("vocab_importer.main.client.chat.completions.create")
def test_generate_vocab_with_rate_limit(mock_create):
    mock_create.side_effect = Exception("Rate limit exceeded")

    result = generate_vocab_with_openai()

    assert "error" in result
    assert "Rate limit exceeded" in result["error"]


@patch("vocab_importer.main.client.chat.completions.create")
def test_generate_vocab_with_invalid_json(mock_create):
    # Create mock response with invalid JSON
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Invalid JSON"))]
    mock_create.return_value = mock_response

    result = generate_vocab_with_openai()

    assert "error" in result
    assert "Invalid JSON response" in result["error"]


@pytest.mark.asyncio
async def test_export_vocabulary():
    app = create_app()
    client = TestClient(app)

    # Mock the backend service response
    mock_data = {"groups": [{"group": "Test Group", "words": ["test1", "test2"]}]}

    with patch("src.services.backend_service.get_vocabulary") as mock_get:
        mock_get.return_value = mock_data
        response = client.get("/export")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "vocabulary_export_" in response.headers["content-disposition"]

        # Verify content
        content = json.loads(response.content)
        assert content == mock_data
