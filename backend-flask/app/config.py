"""Application configuration."""

# app/config.py
import os
from datetime import timedelta
from os import path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Base directory of the project
    BASE_DIR = path.abspath(path.dirname(__file__))

    # Path to the SQLite database file (located in the project root)
    # Updated from "words.db" to "app.db" for consistency.
    DB_PATH = path.join(BASE_DIR, "..", "app.db")

    # (If using SQLAlchemy, you might define the URI like so)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Rate limiting (example: 200 requests per day; 50 per hour)
    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    # Logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }

    # Guardrail configuration
    GUARDRAILS = {
        "min_query_length": 3,
        "max_query_length": 500,
        "default_formality": True,
        "enable_diacritic_check": True,
        "enable_topic_filter": True,
        "enable_profanity_filter": True,
    }


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False


def get_config(config_name):
    """Get configuration by name."""
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    return config_map.get(config_name, DevelopmentConfig)
