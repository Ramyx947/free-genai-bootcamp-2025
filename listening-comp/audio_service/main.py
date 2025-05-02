"""
Audio Module Microservice
Handles TTS generation using Amazon Polly
"""
import sys
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables at module level
load_dotenv()

class TTSRequest(BaseModel):
    text: str
    cache_key: Optional[str] = None

class AudioGenerator:
    def __init__(self):
        try:
            # Verify credentials are loaded
            if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
                raise Exception("AWS credentials not found in environment variables")
            
            print("Initializing AudioGenerator...")
            print(f"AWS Access Key ID exists: {bool(os.getenv('AWS_ACCESS_KEY_ID'))}")
            print(f"AWS Secret Access Key exists: {bool(os.getenv('AWS_SECRET_ACCESS_KEY'))}")
            print(f"AWS Region: {os.getenv('AWS_DEFAULT_REGION', 'us-east-1')}")
            
            # Initialize Polly client
            self.polly = boto3.client(
                'polly',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            )
            
            # Create audio output directory
            self.output_dir = Path("../frontend/static/audio")
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            print(f"Error initializing AudioGenerator: {str(e)}")
            raise

    def generate_tts(self, text: str, cache_key: Optional[str] = None) -> str:
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"audio_{timestamp}.mp3"
            
            # Generate audio with Polly using standard engine
            response = self.polly.synthesize_speech(
                Engine='standard',
                LanguageCode='ro-RO',
                Text=text,
                OutputFormat='mp3',
                VoiceId='Carmen'
            )
            
            # Save audio to file
            if "AudioStream" in response:
                with open(output_file, 'wb') as f:
                    f.write(response['AudioStream'].read())
                return str(output_file)
            else:
                raise Exception("No audio stream in response")
                
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            raise

app = FastAPI()

# Initialize audio module with better error handling
try:
    audio_module = AudioGenerator()
except Exception as e:
    print(f"Failed to initialize AudioGenerator: {str(e)}")
    sys.exit(1)

@app.post("/generate-audio")
async def create_audio(request: TTSRequest):
    try:
        print(f"Received request to generate audio for text: {request.text}")
        audio_data = audio_module.generate_tts(request.text, request.cache_key)
        print(f"Successfully generated audio: {audio_data}")
        return {
            "status": "success",
            "audio_data": audio_data,
            "message": "Audio generated successfully"
        }
    except Exception as e:
        print(f"Error in create_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
