import logging
from typing import Callable, Dict, Optional

logger = logging.getLogger(__name__)


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
async def generate_vocabulary(
    prompt: Optional[str] = None, generator: Callable = default_generate_vocab
) -> Dict:
    """Generate vocabulary using OpenAI.

    Args:
        prompt: Optional custom prompt for vocabulary generation
        generator: Function to generate vocabulary (for testing)

    Returns:
        Dict containing generated vocabulary groups or error message
    """
    try:
        result = await generator(prompt)

        # Validate response format
        if not isinstance(result, dict) or "groups" not in result:
            logger.error(f"Invalid response format from OpenAI: {result}")
            return {"error": "Invalid response format from OpenAI"}

        return result

    except Exception as e:
        logger.error(f"Error generating vocabulary: {str(e)}")
        return {"error": str(e)}
