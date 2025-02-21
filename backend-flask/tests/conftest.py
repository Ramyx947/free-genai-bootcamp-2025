import pytest
import sqlite3
import os
from app import create_app
from app.config import Config
import json
from datetime import datetime

@pytest.fixture
def app():
    # Use test database
    Config.DB_PATH = "test_words.db"
    
    app = create_app()
    app.config['TESTING'] = True
    app.url_map.strict_slashes = False
    
    # Set up test database
    conn = sqlite3.connect(Config.DB_PATH)
    with app.open_resource('../migrations/001_init.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    with app.open_resource('../migrations/002_create_tables.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()
    
    yield app
    
    # Clean up test database
    os.remove(Config.DB_PATH)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_data(app):
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    # Insert test word
    cursor.execute("""
        INSERT INTO words (romanian, english, pronunciation, part_of_speech, parts, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "măr",
        "apple",
        "mur",
        "noun",
        json.dumps(["fruit"]),
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    
    # Insert test group
    cursor.execute("""
        INSERT INTO groups (name, description, word_count, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Test Group",
        "Test Description",
        0,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close() 