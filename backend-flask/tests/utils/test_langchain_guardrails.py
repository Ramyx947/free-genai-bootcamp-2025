import pytest
from unittest.mock import patch, MagicMock
from app.utils.langchain_guardrails import LangChainRomanianGuardrails


@pytest.fixture
def guardrails():
    """Create a LangChainRomanianGuardrails instance for testing."""
    with patch("app.utils.langchain_guardrails.ChatOpenAI"):
        guardrails = LangChainRomanianGuardrails(api_key="sk-test-key")

        # Mock the chains
        mock_moderation_chain = MagicMock()
        mock_formality_chain = MagicMock()

        guardrails.moderation_chain = mock_moderation_chain
        guardrails.formality_chain = mock_formality_chain

        return guardrails


def test_validate_input_success(guardrails):
    """Test successful input validation."""
    guardrails.moderation_chain.invoke.return_value = "SAFE"

    result = guardrails.validate_input("How do I learn Romanian?")
    assert result is True
    guardrails.moderation_chain.invoke.assert_called_once()


def test_validate_input_unsafe(guardrails):
    """Test unsafe input validation."""
    guardrails.moderation_chain.invoke.return_value = (
        "UNSAFE: contains inappropriate content"
    )

    with pytest.raises(ValueError) as excinfo:
        guardrails.validate_input("Some inappropriate text")
    assert "inappropriate content" in str(excinfo.value)
    guardrails.moderation_chain.invoke.assert_called_once()


def test_process_output_formality(guardrails):
    """Test output processing with formality correction."""
    guardrails.formality_chain.invoke.return_value = "dumneavoastră sunteți student"

    result = guardrails.process_output("tu ești student", formal=True)
    assert "dumneavoastră sunteți" in result
    guardrails.formality_chain.invoke.assert_called_once()


def test_process_output_diacritics(guardrails):
    """Test output processing with diacritic correction."""
    # Configure the formality chain to return the input with diacritics fixed
    guardrails.formality_chain.invoke.side_effect = (
        lambda x: "București este capitala României"
    )

    result = guardrails.process_output("Bucuresti este capitala Romaniei")
    assert "București" in result
    assert "României" in result
