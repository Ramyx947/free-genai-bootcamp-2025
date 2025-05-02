# Import from existing service modules
from audio_service.main import AudioGenerator as TTSService
from app.services.question_generator import QuestionGenerator
from app.services.aws_polly import PollyGenerator
from app.services.transcript_processor import TranscriptProcessor

# Define what gets exported when using "from services import *"
__all__ = ['QuestionGenerator', 'PollyGenerator', 'TranscriptProcessor']