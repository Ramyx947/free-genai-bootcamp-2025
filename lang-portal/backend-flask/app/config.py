# app/config.py
import os

class Config:
    # Base directory of the project
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Path to the SQLite database file (located in the project root)
    DB_PATH = os.path.join(BASE_DIR, '..', 'words.db')
    
    # (If using SQLAlchemy, you might define the URI like so)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    
    # Rate limiting (example: 200 requests per day; 50 per hour)
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
