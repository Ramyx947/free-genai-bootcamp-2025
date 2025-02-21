Below is a detailed, step‐by‐step plan for a junior developer to implement the backend API (per the provided <backend-specs>) and to test its successful implementation. This plan follows best practices for Python and Flask and uses Poetry for dependency management.

---

## 1. Project Setup

### 1.1. Create the Project Directory
- Create a folder (e.g., `romanian-learning-backend`).
- Initialize a Git repository and commit the initial structure.

### 1.2. Set Up Poetry for Dependency Management
- **Install Poetry** (if not already installed):
  - Follow instructions at [python-poetry.org](https://python-poetry.org/docs/).
- **Initialize a new Poetry project:**
  ```bash
  poetry init --no-interaction
  ```
- **Add required dependencies** using Poetry:
  ```bash
  poetry add Flask flask-jwt-extended flask-cors Flask-Limiter
  ```
  *(You might also add packages like PyJWT, and any other needed libraries.)*
- **Create a virtual environment** automatically managed by Poetry:
  ```bash
  poetry shell
  ```

---

## 2. Project Structure

Organize the project with clear folders for application code, migrations, seeds, tests, and tasks.

```
romanian-learning-backend/
├── app/
│   ├── __init__.py         # Initializes the Flask app & extensions
│   ├── config.py           # Configuration settings (DB file, JWT secret, etc.)
│   ├── models.py           # Database models and schema setup
│   ├── routes/             # Contains Flask Blueprints for different endpoint groups
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── groups.py
│   │   ├── words.py
│   │   ├── activities.py
│   │   ├── sessions.py
│   │   ├── review.py
│   │   └── footer.py
│   └── utils/              # Helper functions (error handlers, database helpers, etc.)
│       └── errors.py
├── migrations/             # SQL migration files (e.g., 001_init.sql, 002_create_tables.sql)
├── seeds/                  # JSON seed files for populating the database
├── tests/                  # Unit and integration tests
│   ├── __init__.py
│   └── test_api.py
├── tasks.py                # Invoke tasks for init/migrate/seed
├── pyproject.toml          # Managed by Poetry
└── README.md
```

*Tip: Using Flask Blueprints (one per endpoint group) helps keep your code modular and maintainable.*

---

## 3. Database Setup

### 3.1. SQLite3 Configuration
- In `app/config.py`, define the database file (e.g., `words.db`) and other configurations (JWT secret key, rate limit settings, etc.).

### 3.2. Migrations
- Create migration files inside the `migrations/` folder:
  - **001_init.sql** – May include commands to enable foreign key support.
  - **002_create_tables.sql** – Contains SQL commands to create the tables: `words`, `groups`, `words_groups`, `study_sessions`, `study_activities`, `word_review_items`.
- **Write a migration runner** in your tasks (or as a separate script) that reads these SQL files in order and executes them against `words.db`.

### 3.3. Seeding
- Place JSON seed files in the `seeds/` folder.
- Create a seed script that reads these files and populates the database tables.
- Ensure the seed script uses a clear DSL format (see provided example in the specs).

---

## 4. Implementing the API Endpoints

### 4.1. Flask Application Initialization
- In `app/__init__.py`, create the Flask app and register blueprints:
  ```python
  from flask import Flask
  from .config import Config
  from .routes.auth import auth_bp
  from .routes.dashboard import dashboard_bp
  # ... import other blueprints

  def create_app():
      app = Flask(__name__)
      app.config.from_object(Config)

      # Initialize extensions (JWT, CORS, Rate Limiter)
      # e.g., jwt = JWTManager(app)
      #       CORS(app)
      #       limiter = Limiter(app, key_func=get_remote_address)

      # Register blueprints
      app.register_blueprint(auth_bp, url_prefix='/api/auth')
      app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
      # ... register other blueprints for groups, words, activities, sessions, review, footer

      # Register error handlers (in app/utils/errors.py)
      return app
  ```

### 4.2. Create API Routes by Blueprint
- **Authentication (app/routes/auth.py):**
  - Implement `/login` and `/refresh` routes using Flask-JWT-Extended.
- **Dashboard (app/routes/dashboard.py):**
  - Implement a GET endpoint `/api/dashboard` to return overview stats.
- **Word Groups (app/routes/groups.py):**
  - Implement GET, POST, PUT, DELETE endpoints for groups.
  - Implement GET `/api/groups/:id/words` for words in a group.
- **Word Collection (app/routes/words.py):**
  - Implement GET, POST, PUT, DELETE endpoints for vocabulary words.
- **Study Activities (app/routes/activities.py):**
  - Implement GET `/api/activities`, POST `/api/activities/:id/start`, and POST `/api/activities/:id/submit`.
- **Learning Sessions (app/routes/sessions.py):**
  - Implement GET endpoints to list sessions and get session details.
- **Word Review (app/routes/review.py):**
  - Implement POST `/api/study_sessions/:session_id/words/:word_id/review`.
- **Footer (app/routes/footer.py):**
  - Implement GET `/api/footer` to return footer content.

*Tip: Each route should validate input, interact with the database, and return JSON responses following the defined error structure.*

### 4.3. Error Handling
- In `app/utils/errors.py`, create custom error handlers:
  ```python
  from flask import jsonify

  def handle_error(error_code, message, details=None):
      response = {
          "code": error_code,
          "message": message,
          "details": details or {}
      }
      return jsonify(response), 400

  # Then register error handlers for common errors (e.g., 404, 500)
  ```

---

## 5. Task Automation Using Invoke

### 5.1. Create `tasks.py`
- Define tasks for initializing, migrating, and seeding the database.
- Example using Invoke:
  ```python
  from invoke import task
  import sqlite3
  import os

  DB_FILE = 'words.db'
  MIGRATIONS_DIR = 'migrations'
  SEEDS_DIR = 'seeds'

  @task
  def init_db(c):
      """Initialize the SQLite database."""
      if os.path.exists(DB_FILE):
          os.remove(DB_FILE)
      conn = sqlite3.connect(DB_FILE)
      conn.execute("PRAGMA foreign_keys = ON;")
      conn.commit()
      conn.close()
      print("Database initialized.")

  @task
  def migrate(c):
      """Run migration SQL files in order."""
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      for filename in sorted(os.listdir(MIGRATIONS_DIR)):
          if filename.endswith('.sql'):
              with open(os.path.join(MIGRATIONS_DIR, filename), 'r') as sql_file:
                  sql_script = sql_file.read()
                  cursor.executescript(sql_script)
                  print(f"Ran migration: {filename}")
      conn.commit()
      conn.close()

  @task
  def seed(c):
      """Load seed JSON files to populate the database."""
      # Implement logic to read each JSON file in SEEDS_DIR and insert data.
      print("Seeding database...")
      # [Your seeding code here]
  ```
- Run tasks with:
  ```bash
  invoke init_db
  invoke migrate
  invoke seed
  ```

---

## 6. Testing the Implementation

### 6.1. Manual Testing
- **Run the Flask App Locally:**
  - In your main entry file (e.g., `app.py`), call `create_app()` and run the development server.
  - Use commands like:
    ```bash
    poetry run python app.py
    ```
- **Test API Endpoints Manually:**
  - Use tools like [Postman](https://www.postman.com/) or `curl` to send requests to each endpoint.
  - Verify that responses match the expected JSON structures as defined in the specs.

### 6.2. Automated Testing
- **Set Up a Testing Framework:**
  - Install pytest:
    ```bash
    poetry add --dev pytest pytest-flask
    ```
- **Write Test Cases:**
  - Create test files under the `tests/` directory (e.g., `tests/test_api.py`).
  - Use Flask’s test client to simulate API requests:
    ```python
    import pytest
    from app import create_app

    @pytest.fixture
    def client():
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_dashboard_endpoint(client):
        response = client.get('/api/dashboard')
        assert response.status_code == 200
        data = response.get_json()
        # Assert expected keys in the JSON response
        assert "lastSession" in data
        assert "progress" in data
        assert "stats" in data
    ```
- **Run the Tests:**
  ```bash
  poetry run pytest
  ```

### 6.3. Integration & End-to-End Testing
- After unit tests, manually test a full workflow:
  1. **Seed the database** (using your Invoke tasks).
  2. **Login** to get JWT tokens.
  3. **Access protected endpoints** with the JWT token.
  4. **Perform CRUD operations** on words and groups.
  5. **Start a study session, record word reviews, and check session details.**

---

## 7. Best Practices and Final Touches

- **Environment Variables:**  
  Use a `.env` file or similar to manage sensitive configuration (JWT secret, database path) and load these using Python’s `os.environ`.

- **Logging:**  
  Integrate logging (using Python’s `logging` module) to capture errors and important events.

- **Documentation:**  
  Update the `README.md` with clear instructions on:
  - Setting up the project with Poetry.
  - Running migration and seed tasks.
  - Starting the Flask server.
  - Running tests.

- **Code Quality:**  
  Use linters (like Flake8) and formatters (like Black) to ensure code consistency and readability.

- **Version Control:**  
  Commit frequently and write descriptive commit messages.

---

By following this detailed plan, you will:
- Set up a maintainable Python/Flask project using Poetry.
- Implement a modular API following the provided <backend-specs>.
- Automate database migrations and seeding using Invoke tasks.
- Thoroughly test each endpoint using both manual and automated methods.

This approach ensures that the backend is built with best practices and is robust, maintainable, and ready for integration with the frontend.