from unittest.mock import AsyncMock

import pytest

from app.services.openai_service import generate_vocabulary


@pytest.fixture
def mock_generator():
    async def mock_generate(prompt: str = None):
        return {
            "groups": [
                {"group": "Basic Greetings", "words": ["hello", "goodbye"]},
                {"group": "Numbers", "words": ["one", "two"]},
            ]
        }

    return AsyncMock(side_effect=mock_generate)


@pytest.mark.asyncio
async def test_generate_vocabulary_success(mock_generator):
    """Test successful vocabulary generation."""
    result = await generate_vocabulary(generator=mock_generator)

    assert "groups" in result
    assert len(result["groups"]) == 2
    mock_generator.assert_called_once_with(None)


@pytest.mark.asyncio
async def test_generate_vocabulary_with_prompt(mock_generator):
    """Test vocabulary generation with custom prompt."""
    test_prompt = "Generate Romanian food vocabulary"

    result = await generate_vocabulary(prompt=test_prompt, generator=mock_generator)

    assert "groups" in result
    mock_generator.assert_called_once_with(test_prompt)


@pytest.mark.asyncio
async def test_generate_vocabulary_error_handling(mock_generator):
    """Test error handling during vocabulary generation."""
    mock_generator.side_effect = Exception("API Error")

    result = await generate_vocabulary(generator=mock_generator)

    assert "error" in result
    assert "API Error" in result["error"]


@pytest.mark.asyncio
async def test_generate_vocabulary_invalid_response(mock_generator):
    """Test handling of invalid response format."""
    mock_generator.side_effect = lambda x: {"invalid": "format"}

    result = await generate_vocabulary(generator=mock_generator)

    assert "error" in result
    assert "Invalid response format" in result["error"]
