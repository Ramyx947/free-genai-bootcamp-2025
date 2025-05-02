import gradio as gr
import soundfile as sf
import json
import random
import tempfile
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client correctly
client = OpenAI(
    api_key=openai_api_key,
    base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
)

# Load Romanian traditions data
with open("romanian_traditions.json", "r", encoding='utf-8') as f:
    traditions_data = json.load(f)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_audio(audio_filepath, context_text):
    try:
        data, samplerate = sf.read(audio_filepath)
        duration = len(data) / samplerate
        
        if duration > 60:
            data = data[:int(samplerate * 60)]
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            sf.write(temp_file.name, data, samplerate)
            audio_to_transcribe = temp_file.name
        else:
            audio_to_transcribe = audio_filepath

        # Transcribe audio
        with open(audio_to_transcribe, "rb") as audio_file:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ro",
                response_format="json"
            )
            transcription = transcript_response.text

        # Evaluate speaking
        evaluation_prompt = (
            "Please evaluate the following Romanian speaking transcript based on: "
            "1. Fluency and Coherence "
            "2. Lexical Resource "
            "3. Grammatical Range and Accuracy "
            f"Transcript: {transcription}. "
            f"Context: {context_text}"
        )

        evaluation_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Romanian language examiner."},
                {"role": "user", "content": evaluation_prompt}
            ]
        )
        
        return {
            "transcription": transcription,
            "evaluation": evaluation_response.choices[0].message.content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/evaluate-speaking")
async def evaluate_speaking(audio_data: dict):
    try:
        logger.info("Received speaking evaluation request")
        
        if not audio_data.get("audio"):
            logger.error("No audio data received")
            raise HTTPException(status_code=400, detail="No audio data provided")
            
        # Add your speech evaluation logic here
        logger.info("Processing audio data...")
        
        return {
            "score": 85,
            "feedback": "Good pronunciation!"
        }
        
    except Exception as e:
        logger.error(f"Error evaluating speaking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/speaking-prompts")
async def get_speaking_prompts():
    return traditions_data 

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 