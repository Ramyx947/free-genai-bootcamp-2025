import logging
import os
from typing import Dict, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

# Global client variable to allow for easier patching in tests
_client = None


def get_openai_client():
    """Get or create an OpenAI client instance."""
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY", "dummy_key_for_tests")
        _client = OpenAI(api_key=api_key)
    return _client


# Default implementation that will be replaced in tests
async def default_generate_vocab(prompt: Optional[str] = None) -> Dict:
    try:
        from vocab_importer.main import generate_vocab_with_openai

        return await generate_vocab_with_openai(prompt)
    except ImportError:
        # Return mock data for testing
        return {
            "groups": [
                {"group": "Basic Greetings", "words": ["hello", "goodbye"]},
                {"group": "Numbers", "words": ["one", "two"]},
            ]
        }


# Service that accepts the generator function
async def generate_vocabulary(prompt: str, formal: bool = True) -> Dict:
    """Generate vocabulary using OpenAI."""
    try:
        # Get client instance
        client = get_openai_client()

        # Using the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return {"response": response.choices[0].message.content, "status": "success"}
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
