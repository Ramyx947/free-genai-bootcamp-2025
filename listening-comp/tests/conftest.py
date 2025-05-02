import pytest
from pathlib import Path
import sys

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

# Import services
from audio_service.polly_generator import AudioGenerator
from question_service.question_generator import QuestionGenerator
from transcript_service.youtube_processor import YouTubeProcessor

@pytest.fixture
def audio_generator():
    return AudioGenerator()

@pytest.fixture
def question_generator():
    return QuestionGenerator()

@pytest.fixture
def youtube_processor():
    return YouTubeProcessor() 