import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import create_app, generate_vocab_with_openai


def test_generate_vocab_with_openai_development_mode():
    with patch.dict("os.environ", {"DEVELOPMENT_MODE": "true"}):
        result = generate_vocab_with_openai()
        assert "groups" in result
        assert len(result["groups"]) == 2
        assert result["groups"][0]["group"] == "Basic Greetings"


@patch("src.main.get_openai_client")
def test_generate_vocab_with_openai_api_call(mock_client):
    # Create mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content='{"groups": [{"group": "Test Group", "words": ["test1", "test2"]}]}'
            )
        )
    ]
    mock_client.return_value.chat.completions.create.return_value = mock_response

    result = generate_vocab_with_openai()

    # Verify result
    assert "groups" in result
    assert len(result["groups"]) == 1
    assert result["groups"][0]["group"] == "Test Group"


@patch("src.main.get_openai_client")
def test_generate_vocab_with_openai_error_handling(mock_client):
    mock_client.return_value.chat.completions.create.side_effect = Exception(
        "API Error"
    )

    result = generate_vocab_with_openai()
    assert "error" in result
    assert "API Error" in result["error"]


@patch("src.main.get_openai_client")
def test_generate_vocab_with_custom_prompt(mock_client):
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
    mock_client.return_value.chat.completions.create.return_value = mock_response

    result = generate_vocab_with_openai(prompt=custom_prompt)

    assert "groups" in result
    assert result["groups"][0]["group"] == "Animals"


@patch("src.main.get_openai_client")
def test_generate_vocab_with_rate_limit(mock_client):
    mock_client.return_value.chat.completions.create.side_effect = Exception(
        "Rate limit exceeded"
    )

    result = generate_vocab_with_openai()

    assert "error" in result
    assert "Rate limit exceeded" in result["error"]


@patch("src.main.get_openai_client")
def test_generate_vocab_with_invalid_json(mock_client):
    # Create mock response with invalid JSON
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Invalid JSON"))]
    mock_client.return_value.chat.completions.create.return_value = mock_response

    result = generate_vocab_with_openai()

    assert "error" in result
    assert "Invalid JSON response" in result["error"]


@pytest.mark.asyncio
async def test_export_vocabulary():
    """Test the export vocabulary endpoint."""
    app = create_app()

    # Mock data
    mock_data = {"groups": [{"group": "Test Group", "words": ["test1", "test2"]}]}

    # Create mock using AsyncMock
    mock_get = AsyncMock()
    mock_get.return_value = mock_data

    # Patch at the correct level
    with patch("src.main.get_vocabulary", mock_get):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/export")

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/json"
            assert "vocabulary_export_" in response.headers["content-disposition"]

            content = response.json()
            assert content == mock_data

    # Verify mock was called
    mock_get.assert_awaited_once()
