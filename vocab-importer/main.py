# Standard library imports
import csv
import io
import json
import os
from typing import List, Optional

import PyPDF2

# Third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI

load_dotenv()

app = FastAPI(title="Vocab Importer")
templates = Jinja2Templates(directory="templates")

# Set up static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set your OpenAI API key from the environment.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), organization=os.environ.get("ORG_ID")
)

# Global storage for the generated vocabulary.
vocab_data = []


def generate_vocab_with_openai(prompt=None):
    """Call OpenAI's ChatCompletion endpoint to generate vocabulary groups."""
    if os.environ.get("DEVELOPMENT_MODE") == "true":
        return {
            "groups": [
                {
                    "group": "Basic Greetings",
                    "words": ["hello", "hi", "goodbye", "bye"],
                },
                {"group": "Numbers", "words": ["one", "two", "three", "four"]},
            ]
        }

    if prompt is None:
        prompt = (
            "Generate a list of vocabulary groups for a language learning app. "
            "Each group should have a 'group' key and a 'words' key "
            "which is a list of words. "
            "Return the output in valid JSON format."
        )

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that generates vocabulary groups.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )

        content = completion.choices[0].message.content.strip()
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return {"error": str(e)}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "vocab_data": vocab_data}
    )


@app.post("/generate")
async def generate_vocab(prompt: Optional[str] = Form(None)):
    result = generate_vocab_with_openai(prompt)
    if "error" in result:
        return JSONResponse(content=result, status_code=400)
    vocab_data.extend(result.get("groups", []))
    return RedirectResponse(url="/", status_code=303)


def parse_file_content(content: bytes, file_type: str) -> List[dict]:
    """Parse different file formats into vocabulary data."""
    if file_type == "application/json":
        return json.loads(content.decode())

    vocab_data = []
    if file_type == "text/plain":
        # Parse TXT - assume tab or comma separated: word,translation
        lines = content.decode().splitlines()
        for line in lines:
            if "," in line:
                word, translation = line.split(",", 1)
            elif "\t" in line:
                word, translation = line.split("\t", 1)
            else:
                continue
            vocab_data.append(
                {
                    "group": "Imported Words",
                    "words": [word.strip(), translation.strip()],
                }
            )

    elif file_type == "text/csv":
        # Parse CSV
        csv_file = io.StringIO(content.decode())
        reader = csv.DictReader(csv_file)
        current_group = None
        words = []

        for row in reader:
            if "group" in row and row["group"]:
                if current_group and words:
                    vocab_data.append({"group": current_group, "words": words})
                current_group = row["group"]
                words = []
            if "word" in row and "translation" in row:
                words.append([row["word"].strip(), row["translation"].strip()])

        if current_group and words:
            vocab_data.append({"group": current_group, "words": words})

    elif file_type == "application/pdf":
        # Parse PDF
        pdf_file = io.BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Split by lines and parse each line
        lines = text.splitlines()
        current_group = "PDF Import"
        words = []

        for line in lines:
            if ":" in line:  # Assume group headers end with colon
                if current_group and words:
                    vocab_data.append({"group": current_group, "words": words})
                current_group = line.strip(":")
                words = []
            elif "," in line or "\t" in line:
                if "," in line:
                    word, translation = line.split(",", 1)
                else:
                    word, translation = line.split("\t", 1)
                words.append([word.strip(), translation.strip()])

        if current_group and words:
            vocab_data.append({"group": current_group, "words": words})

    return {"groups": vocab_data}


@app.post("/import")
async def import_vocab(request: Request, file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = parse_file_content(content, file.content_type)
        vocab_data.extend(result.get("groups", []))
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Error importing vocabulary: {str(e)}"}, status_code=400
        )


@app.get("/export")
async def export_vocab():
    response = JSONResponse(content={"groups": vocab_data})
    response.headers["Content-Disposition"] = "attachment; filename=vocab.json"
    return response
