import os
from pathlib import Path

# Test configuration
TEST_CONFIG = {
    "AUDIO_SERVICE_URL": "http://localhost:8003",
    "QUESTION_SERVICE_URL": "http://localhost:8002",
    "TRANSCRIPT_SERVICE_URL": "http://localhost:8001",
    
    "TEST_DATA_DIR": Path(__file__).parent.parent / "data" / "test",
    "TEST_AUDIO_DIR": Path(__file__).parent.parent / "data" / "test" / "audio",
    "TEST_TRANSCRIPT_DIR": Path(__file__).parent.parent / "data" / "test" / "transcripts",
    
    "AWS_REGION": "us-east-1",
    "POLLY_VOICE_ID": "Carmen",
    "LANGUAGE_CODE": "ro-RO"
}

# Create test directories
for dir_path in [TEST_CONFIG["TEST_DATA_DIR"], 
                 TEST_CONFIG["TEST_AUDIO_DIR"],
                 TEST_CONFIG["TEST_TRANSCRIPT_DIR"]]:
    dir_path.mkdir(parents=True, exist_ok=True) 