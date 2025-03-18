import pytest
from unittest.mock import patch, MagicMock
from app.services.openai_service import generate_vocabulary


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client for testing."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Here is some Romanian vocabulary"))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.mark.asyncio
async def test_generate_vocabulary_success(mock_openai_client):
    """Test successful vocabulary generation."""
    with patch(
        "app.services.openai_service.get_openai_client", return_value=mock_openai_client
    ):
        result = await generate_vocabulary("Test prompt")
        assert "response" in result
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_generate_vocabulary_with_prompt(mock_openai_client):
    """Test vocabulary generation with custom prompt."""
    test_prompt = "Generate Romanian food vocabulary"

    with patch(
        "app.services.openai_service.get_openai_client", return_value=mock_openai_client
    ):
        result = await generate_vocabulary(test_prompt)
        assert "response" in result

        # Verify the prompt was passed correctly
        mock_openai_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": test_prompt}],
            temperature=0.7,
        )


@pytest.mark.asyncio
async def test_generate_vocabulary_error_handling():
    """Test error handling during vocabulary generation."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    with patch(
        "app.services.openai_service.get_openai_client", return_value=mock_client
    ):
        with pytest.raises(Exception):
            await generate_vocabulary("Test prompt")


@pytest.mark.asyncio
async def test_generate_vocabulary_invalid_response():
    """Test handling of invalid response format."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    # Create an invalid response structure
    mock_response.choices = []  # Empty choices
    mock_client.chat.completions.create.return_value = mock_response

    with patch(
        "app.services.openai_service.get_openai_client", return_value=mock_client
    ):
        with pytest.raises(IndexError):
            await generate_vocabulary("Test prompt")
