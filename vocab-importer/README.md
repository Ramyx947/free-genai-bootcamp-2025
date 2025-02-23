# Vocab Importer

An internal tool to help manage vocabulary for a language learning app. This app uses FastAPI and OpenAI's API to let you:

- **Generate Vocabulary:** Create word groups using OpenAI's ChatCompletion API with the `gpt-4o-mini` model.
- **Import Vocabulary:** Upload a JSON file to add new words.
- **Export Vocabulary:** Download the current word list as a JSON file.

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