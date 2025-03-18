import pytest
from unittest.mock import patch, MagicMock
from app.services.openai_service import (
    generate_vocabulary,
    default_generate_vocab,
    get_openai_client,
)


@pytest.mark.asyncio
async def test_generate_vocabulary_success():
    """Test successful vocabulary generation"""
    # Create a mock response structure that matches the new OpenAI API
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Here is some Romanian vocabulary"))
    ]

    # Create a mock client with a mock chat completions create method
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    # Patch the get_openai_client function to return our mock client
    with patch(
        "app.services.openai_service.get_openai_client", return_value=mock_client
    ):
        result = await generate_vocabulary("Teach me about verbs", formal=True)

        # Verify the result
        assert "response" in result
        assert result["status"] == "success"

        # Verify correct parameters were passed
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Teach me about verbs"}],
            temperature=0.7,
        )


@pytest.mark.asyncio
async def test_generate_vocabulary_error():
    """Test error handling in vocabulary generation"""
    # Create a mock client that raises an exception
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    # Patch the get_openai_client function
    with patch(
        "app.services.openai_service.get_openai_client", return_value=mock_client
    ):
        with pytest.raises(Exception):
            await generate_vocabulary("Test prompt", formal=True)


@pytest.mark.asyncio
async def test_openai_client_is_mocked():
    """Test that the OpenAI client is properly mocked"""
    # Get the client
    from app.services.openai_service import get_openai_client

    client = get_openai_client()

    # Verify it's a MagicMock
    from unittest.mock import MagicMock

    assert isinstance(client, MagicMock)

    # Verify it doesn't make real API calls
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Test"}]
    )

    # Verify the response is mocked
    assert isinstance(response, MagicMock)
    assert isinstance(response.choices[0].message.content, str)


@pytest.mark.asyncio
async def test_default_generate_vocab():
    """Test the default_generate_vocab function"""
    # Test with a prompt
    result = await default_generate_vocab("Test prompt")
    assert "groups" in result
    assert isinstance(result["groups"], list)
    assert len(result["groups"]) > 0

    # Test without a prompt
    result = await default_generate_vocab()
    assert "groups" in result
    assert isinstance(result["groups"], list)
    assert len(result["groups"]) > 0


def test_get_openai_client_singleton():
    """Test that get_openai_client returns a singleton"""
    # Reset the client
    import app.services.openai_service

    app.services.openai_service._client = None

    # Patch the OpenAI class
    with patch("app.services.openai_service.OpenAI") as mock_openai:
        # First call should create a new client
        client1 = get_openai_client()
        assert mock_openai.called

        # Reset the mock
        mock_openai.reset_mock()

        # Second call should return the existing client
        client2 = get_openai_client()
        assert not mock_openai.called
        assert client1 == client2
