import boto3
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from app.core.config import Config

class PollyGenerator:
    def __init__(self):
        self.client = boto3.client(
            'polly',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION
        )
        
        self.voices = {
            'male': ['Radu'],  # Romanian male voice
            'female': ['Carmen'],  # Romanian female voice
            'default': 'Carmen'
        }
        
        self.config = {
            'Engine': 'neural',
            'LanguageCode': 'ro-RO',
            'VoiceId': self.voices['default'],
            'OutputFormat': 'mp3',
            'SampleRate': '24000',
            'TextType': 'text'
        }

    def generate_audio(self, text: str, voice_id: Optional[str] = None) -> Optional[str]:
        """Generate audio file from text using Amazon Polly"""
        try:
            if voice_id:
                self.config['VoiceId'] = voice_id

            response = self.client.synthesize_speech(**self.config, Text=text)
            
            if "AudioStream" in response:
                # Generate unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"audio_{timestamp}.mp3"
                filepath = Config.AUDIO_DIR / filename
                
                # Save audio stream to file
                with open(filepath, 'wb') as f:
                    f.write(response['AudioStream'].read())
                
                return str(filepath)
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            return None

    def get_voice_for_gender(self, gender: str) -> str:
        """Get appropriate voice for gender"""
        if gender.lower() in ['m', 'male']:
            return self.voices['male'][0]
        elif gender.lower() in ['f', 'female']:
            return self.voices['female'][0]
        return self.voices['default'] 