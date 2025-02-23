from pydantic_settings import BaseSettings
from typing import Set
from functools import lru_cache

class Settings(BaseSettings):
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 