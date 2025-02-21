-- migrations/002_create_tables.sql

-- Create the words table
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    romanian TEXT NOT NULL,
    english TEXT NOT NULL,
    pronunciation TEXT,
    part_of_speech TEXT NOT NULL,
    parts JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the groups table
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    word_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the words_groups join table
CREATE TABLE IF NOT EXISTS words_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY(word_id) REFERENCES words(id),
    FOREIGN KEY(group_id) REFERENCES groups(id)
);

-- Create the study_sessions table
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id TEXT NOT NULL,
    group_id INTEGER,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    score REAL DEFAULT 0,
    FOREIGN KEY(group_id) REFERENCES groups(id)
);

-- Create the study_activities table
CREATE TABLE IF NOT EXISTS study_activities (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK(type IN ('vocabulary', 'reading', 'grammar')),
    title TEXT NOT NULL,
    description TEXT,
    thumbnail_url TEXT,
    progress REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the word_review_items table
CREATE TABLE IF NOT EXISTS word_review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    user_answer TEXT,
    correct_answer TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(word_id) REFERENCES words(id),
    FOREIGN KEY(session_id) REFERENCES study_sessions(id)
);
