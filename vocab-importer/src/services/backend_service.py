import httpx
from ..config import Settings

settings = Settings()

async def get_vocabulary() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.BACKEND_URL}/api/vocabulary"
        )
        response.raise_for_status()
        return response.json()

async def save_vocabulary(vocabulary_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.BACKEND_URL}/api/vocabulary",
            json=vocabulary_data
        )
        response.raise_for_status()
        return response.json() 