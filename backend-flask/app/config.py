# app/config.py
import os
from datetime import timedelta
from os import path


class Config:
    # Base directory of the project
    BASE_DIR = path.abspath(path.dirname(__file__))

    # Path to the SQLite database file (located in the project root)
    DB_PATH = path.join(BASE_DIR, "..", "words.db")

    # (If using SQLAlchemy, you might define the URI like so)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///words.db")
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
