import sqlite3
import json

DB_FILE = 'words.db'

def test_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check that the tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)
    
    # Run a sample query on the words table
    cursor.execute("SELECT id, romanian, english FROM words;")
    words = cursor.fetchall()
    print("Words:", words)
    
    # If there is JSON data, print one entry parsed as JSON
    cursor.execute("SELECT parts FROM words LIMIT 1;")
    result = cursor.fetchone()
    if result:
        parts = json.loads(result[0])
        print("Sample parts data:", parts)
    
    conn.close()

if __name__ == "__main__":
    test_database()
