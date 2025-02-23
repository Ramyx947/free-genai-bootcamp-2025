from typing import AsyncGenerator

from httpx import AsyncClient

from .config import Settings


async def get_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as client:
        yield client


async def get_settings() -> Settings:
    return Settings()
