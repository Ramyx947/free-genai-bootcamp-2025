import os
from pathlib import Path
from typing import Dict, List

def create_test_file(content: str, filename: str, directory: Path) -> Path:
    """Create a test file with given content"""
    filepath = directory / filename
    filepath.write_text(content)
    return filepath

def cleanup_test_files(directory: Path, pattern: str = "test_*"):
    """Clean up test files after tests"""
    for file in directory.glob(pattern):
        try:
            file.unlink()
        except Exception as e:
            print(f"Error cleaning up {file}: {e}")

def get_test_audio_path() -> Path:
    """Get path for test audio files"""
    return Path(__file__).parent.parent.parent / "data" / "audio" / "test"

def get_test_transcript_path() -> Path:
    """Get path for test transcript files"""
    return Path(__file__).parent.parent.parent / "data" / "transcripts" / "test" 