from typing import Any, Dict

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings

settings = Settings()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def get_vocabulary() -> Dict[str, Any]:
    """Get vocabulary from backend with retry logic."""
    timeout = httpx.Timeout(10.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(f"{settings.BACKEND_URL}/api/vocabulary")
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise VocabImporterError("Backend service timeout", status_code=504)
        except httpx.NetworkError:
            raise VocabImporterError(
                "Network error connecting to backend", status_code=502
            )


async def save_vocabulary(vocabulary_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.BACKEND_URL}/api/vocabulary", json=vocabulary_data
        )
        response.raise_for_status()
        return response.json()
