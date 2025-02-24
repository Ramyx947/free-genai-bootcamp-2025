from functools import lru_cache
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # OpenAI settings
    PROJECT_ID: str | None = None
    OPENAI_API_KEY: str | None = None
    ORG_ID: str | None = None

    # Service URLs
    BACKEND_URL: str = "http://localhost:5000"
    FRONTEND_URL: str = "http://localhost:5173"

    # File settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: Set[str] = {"json", "txt", "csv", "pdf"}

    # Service settings
    LOG_LEVEL: str = "INFO"
    WORKERS: int = 4
    TIMEOUT: int = 60
    RATE_LIMIT: int = 100  # requests per minute

    # LLM settings
    LLM_ENABLED: bool = False
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 300

    # Replace the old Config class with model_config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",  # This allows extra fields
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
