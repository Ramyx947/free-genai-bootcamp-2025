from fasthtml.common import (
    Div, H2, Pre, Form, Input, Button, A, Response, 
    RedirectResponse, UploadFile, Titled, P, Hr,
    fast_app, serve  # Added these imports
)
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

# Set your OpenAI API key from the environment.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("ORG_ID")
)

# Global storage for the generated vocabulary.
vocab_data = []

def generate_vocab_with_openai(prompt=None):
    """
    Call OpenAI's ChatCompletion endpoint to generate vocabulary groups.
    Using gpt-4-turbo-preview for better results
    """
    # For testing without API calls
    if os.environ.get("DEVELOPMENT_MODE") == "true":
        return {
            "groups": [
                {
                    "group": "Basic Greetings",
                    "words": ["hello", "hi", "goodbye", "bye"]
                },
                {
                    "group": "Numbers",
                    "words": ["one", "two", "three", "four"]
                }
            ]
        }

    if prompt is None:
        prompt = (
            "Generate a list of vocabulary groups for a language learning app. "
            "Each group should have a 'group' key and a 'words' key which is a list of words. "
            "Return the output in valid JSON format."
        )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that generates vocabulary groups."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300,
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return {"error": str(e)}

app, rt = fast_app()

@rt('/')
def get():
    return Titled("Vocab Importer",
        Div(
            H2("Current Vocab"),
            Pre(json.dumps(vocab_data, indent=2)),
            Hr(),  # Changed from HR() to Hr()
            # Form to trigger vocab generation via the LLM
            Form(action="/generate", method="post")(
                Button("Generate Vocab")
            ),
            Hr(),  # Changed from HR() to Hr()
            # Form to import vocab JSON file
            Form(action="/import", method="post", enctype="multipart/form-data")(
                Input(type="file", name="vocab_file"),
                Button("Import Vocab")
            ),
            Hr(),  # Changed from HR() to Hr()
            # Link to export current vocab as JSON
            A(href="/export")("Export Vocab")
        )
    )

@rt('/generate')
def post_generate():
    global vocab_data
    result = generate_vocab_with_openai()
    
    # Check if there was an error
    if 'error' in result:
        return Titled("Generation Error", 
            Div(
                P(f"Failed to generate vocab: {result['error']}"),
                Hr(),
                A(href="/")("Back to Home")
            )
        )
    
    vocab_data = result
    return RedirectResponse(url="/")

@rt('/import')
async def post_import(vocab_file: UploadFile):
    global vocab_data
    file_content = await vocab_file.read()
    try:
        imported_vocab = json.loads(file_content.decode('utf-8'))
        vocab_data = imported_vocab
    except Exception as e:
        return Titled("Import Error", P("Failed to import vocab: " + str(e)))
    return RedirectResponse(url="/")

@rt('/export')
def get_export():
    response = Response(json.dumps(vocab_data, indent=2), media_type="application/json")
    response.headers["Content-Disposition"] = "attachment; filename=vocab.json"
    return response

serve()
