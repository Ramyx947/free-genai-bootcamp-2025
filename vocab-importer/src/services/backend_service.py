from typing import Any, Dict

import httpx
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

from ..config import Settings
from ..errors.exceptions import VocabImporterError

settings = Settings()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True,
)
async def get_vocabulary():
    """Get vocabulary from backend."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.BACKEND_URL}/api/vocabulary",
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise VocabImporterError(f"Error fetching from backend: {str(e)}")
    except Exception as e:
        raise VocabImporterError(f"Unexpected error: {str(e)}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True,
)
async def save_vocabulary(vocabulary_data: dict):
    """Save vocabulary to backend."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.BACKEND_URL}/api/vocabulary", json=vocabulary_data
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise VocabImporterError(f"Error saving to backend: {str(e)}")
    except Exception as e:
        raise VocabImporterError(f"Unexpected error: {str(e)}")
