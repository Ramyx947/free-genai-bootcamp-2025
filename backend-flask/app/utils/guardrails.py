"""Guardrails for Romanian language learning."""

from dataclasses import dataclass
from typing import Optional

# Import and re-export the LangChain guardrails for backward compatibility
from .langchain_guardrails import LangChainRomanianGuardrails


@dataclass
class GuardrailResult:
    """Result of a guardrail check."""

    success: bool
    message: Optional[str] = None
    filtered_content: Optional[str] = None


# Create a compatibility wrapper class
class RomanianGuardrails:
    """Compatibility wrapper for LangChain guardrails."""

    def __init__(self, api_key=None):
        """Initialize the LangChain guardrails."""
        self.api_key = api_key
        self.langchain_guardrails = None

    def _get_guardrails(self):
        """Lazy initialization of guardrails to ensure app context is available."""
        if self.langchain_guardrails is None:
            self.langchain_guardrails = LangChainRomanianGuardrails(
                api_key=self.api_key
            )
        return self.langchain_guardrails

    def validate_input(self, text: str) -> GuardrailResult:
        """Validate user input for Romanian language learning queries."""
        try:
            self._get_guardrails().validate_input(text)
            return GuardrailResult(True, filtered_content=text)
        except ValueError as e:
            return GuardrailResult(False, str(e))

    def process_output(self, text: str, formal: bool = True) -> GuardrailResult:
        """Process and validate AI output for Romanian text."""
        if not text:
            return GuardrailResult(False, "Empty response")

        processed_text = self._get_guardrails().process_output(text, formal)
        return GuardrailResult(True, filtered_content=processed_text)
