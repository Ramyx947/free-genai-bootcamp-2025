import boto3
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

class AudioConfig:
    def __init__(self,
                 voice_id: str = "Carmen",  # Romanian female voice
                 engine: str = "standard",  # Standard engine for Romanian
                 language_code: str = "ro-RO"):
        self.voice_id = voice_id
        self.engine = engine
        self.language_code = language_code

class AudioGenerator:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Polly client
        self.polly = boto3.client(
            'polly',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        
        # Define Romanian voices
        self.voices = {
            'female': ['Carmen'],  # Romanian female voice
            'male': ['Emil'],      # Romanian male voice
            'default': 'Carmen'
        }
        
        # Create audio output directory
        self.audio_dir = Path("../data/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def generate_audio(self, text: str, config: Optional[AudioConfig] = None) -> str:
        """Generate audio using Amazon Polly"""
        if config is None:
            config = AudioConfig()

        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.audio_dir / f"audio_{timestamp}.mp3"
            
            # Generate audio with Polly
            response = self.polly.synthesize_speech(
                Engine=config.engine,
                LanguageCode=config.language_code,
                Text=text,
                OutputFormat='mp3',
                VoiceId=config.voice_id
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
            return None

    def get_voice_for_gender(self, gender: str) -> str:
        """Get appropriate voice for gender"""
        if gender.lower() in ['m', 'male']:
            return self.voices['male'][0]
        elif gender.lower() in ['f', 'female']:
            return self.voices['female'][0]
        return self.voices['default']