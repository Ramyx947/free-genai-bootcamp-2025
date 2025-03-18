"""Application configuration."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-please-change")
    FLASK_APP = "app.py"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenAI
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # Guardrails
    GUARDRAILS_ENABLED = True

    # LangChain
    LANGCHAIN_VERBOSE = False
    LANGCHAIN_PROJECT = "romanian-learning-app"


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # Disable real API calls in tests
    OPENAI_API_KEY = "sk-test-key"

    # Enable guardrails in tests
    GUARDRAILS_ENABLED = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False

    # Use stronger secret key in production
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Database should be configured via DATABASE_URL env var

    # Ensure OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable is required in production"
        )


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
