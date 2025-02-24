import json
import os
import sqlite3

from invoke import task

DB_FILE = "words.db"
MIGRATIONS_DIR = "migrations"
SEEDS_DIR = "seeds"


@task
def init_db(ctx):
    """Initialize the SQLite database (delete existing file if any)."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()
    print("Database initialized.")


@task
def migrate(ctx):
    """Run migration SQL files in order."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for filename in sorted(os.listdir(MIGRATIONS_DIR)):
        if filename.endswith(".sql"):
            file_path = os.path.join(MIGRATIONS_DIR, filename)
            with open(file_path, "r") as sql_file:
                sql_script = sql_file.read()
                cursor.executescript(sql_script)
                print(f"Ran migration: {filename}")
    conn.commit()
    conn.close()


@task
def seed(ctx):
    """Seed the database with initial data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Load seed data from JSON files
    for filename in os.listdir(SEEDS_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(SEEDS_DIR, filename)
            with open(file_path, "r") as f:
                data = json.load(f)

            table_name = filename.replace("_seed.json", "")

            if data:
                # Get columns from first item
                columns = list(data[0].keys())
                placeholders = ",".join(["?" for _ in columns])
                columns_str = ",".join(columns)

                # Insert data
                for item in data:
                    # Convert any list/dict values to JSON strings
                    values = []
                    for col in columns:
                        val = item[col]
                        if isinstance(val, (list, dict)):
                            val = json.dumps(val)
                        values.append(val)

                    query = (
                        f"INSERT INTO {table_name} "
                        f"({columns_str}) "
                        f"VALUES ({placeholders})"
                    )
                    cursor.execute(query, values)

                print(f"Seeded {table_name} table")

    conn.commit()
    conn.close()
    print("Database seeded successfully!")


@task
def test(ctx, coverage=False):
    """Run tests."""
    cmd = "pytest"
    if coverage:
        cmd += " --cov=app" " --cov-report=term-missing" " --cov-report=html"
    ctx.run(cmd)
