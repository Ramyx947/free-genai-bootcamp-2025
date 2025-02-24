# Vocab Importer Service 📚

A service that helps import vocabulary into our Romanian Learning App.

## What It Does 🎯

- Takes vocabulary files (JSON, TXT, CSV, PDF)
- Checks if they're correct
- Sends them to the main app
- Watches for problems
- Tells you if something goes wrong

## Quick Start 🚀

```bash
# Start everything
docker compose up

# Just this service
docker compose up vocab-importer
```

## API Endpoints 🛣️

| What It Does    | Endpoint     | Method |
|----------------|--------------|--------|
| Check health   | /health      | GET    |
| Import file    | /import      | POST   |
| Export vocab   | /export      | GET    |

## Monitoring 📊

We use Prometheus to watch:
- How many requests we get
- How fast we respond
- If anything goes wrong

To see metrics:
1. Go to: http://localhost:5001/metrics
2. Look for:
   - vocab_importer_requests_total
   - vocab_importer_request_latency_seconds

## Testing 🧪

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov

# Test metrics
curl http://localhost:5001/metrics
```

## Features
- File format support: JSON, TXT, CSV, PDF
- Direct integration with backend API
- Validation and error handling
- Health checks for container orchestration

## Configuration
Environment variables:
- BACKEND_URL - Backend API URL
- MAX_FILE_SIZE - Maximum file size (default 10MB)

## Development
```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn src.main:app --reload --port 5001

# Run tests
poetry run pytest
```

## Docker
```bash
# Build
docker build -t vocab-importer .

# Run
docker run -p 5001:5001 vocab-importer
```

## Requirements

- Python 3.7 or higher
- FastAPI framework
- Uvicorn ASGI server
- OpenAI Python library

## Installation

1. **Install FastAPI:**

   ```bash
   pip install fastapi
   ```


2. **Install Uvicorn:**

   ```bash
   pip install uvicorn
   ```


3. **Install OpenAI:**

   ```bash
   pip install openai
   ```


4. **Set Up Environment Variables:**

   - **Create a `.env` File:** This file holds sensitive info like API keys. Don't share it publicly.
   - **Create a `.env.example` File:** List required environment variables without sensitive data. Share this file to help others set up their environment.

   **Example `.env.example`:**

   ```
   OPENAI_API_KEY=
   ORG_ID=
   ```


   **Note:** Add `.env` to your `.gitignore` file to keep it private.

5. **Run the App:**

   ```bash
   uvicorn vocab_importer.main:app --reload --port 5001
   ```


   Access the app at [http://localhost:5001/](http://localhost:5001/).

## Usage

- **Generate Vocabulary:**

  Click "Generate Vocab" on the home page. This uses OpenAI's API with the `gpt-4o-mini` model to create word groups.

  **Important:** You need an active OpenAI API key with credits. Without credits, this feature won't work.

- **Import Vocabulary:**

  Use the upload form to select a JSON file with vocabulary data. Click "Import Vocab" to add the words.

  **Note:** Importing doesn't need an OpenAI API key or credits.

- **Export Vocabulary:**

  Click "Export Vocab" to download the current words as `vocab.json`.

  **Note:** Exporting doesn't need an OpenAI API key or credits.

## Resources

- **Sample Vocab JSON File:** [View here](utils/vocab.json).
- **Vocab Importer Screenshot:** [View here](images/vocab-importer.png).

## License

This project is under the MIT License. See the LICENSE file for details. 