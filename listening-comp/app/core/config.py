import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    # Service Ports
    AUDIO_SERVICE_PORT = 8003
    QUESTION_SERVICE_PORT = 8002
    TRANSCRIPT_SERVICE_PORT = 8001

    # Data Directories
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    AUDIO_DIR = DATA_DIR / 'audio'
    TRANSCRIPT_DIR = DATA_DIR / 'transcripts'
    QUESTION_DIR = DATA_DIR / 'questions'

    # Create directories if they don't exist
    for dir_path in [AUDIO_DIR, TRANSCRIPT_DIR, QUESTION_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
