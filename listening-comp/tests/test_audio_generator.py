import pytest
from pathlib import Path
from backend.audio_generator import AudioGenerator, AudioConfig

def test_audio_generator():
    generator = AudioGenerator()
    
    # Test basic audio generation
    text = "Bună ziua! Acesta este un test."
    audio_file = generator.generate_audio(text)
    
    assert audio_file is not None
    assert Path(audio_file).exists()
    assert Path(audio_file).suffix == '.mp3'
    
    # Test with different voices
    config_male = AudioConfig(voice_id='Emil')
    audio_file_male = generator.generate_audio(text, config_male)
    assert audio_file_male is not None
    
    # Test voice selection by gender
    assert generator.get_voice_for_gender('male') == 'Emil'
    assert generator.get_voice_for_gender('female') == 'Carmen'
    assert generator.get_voice_for_gender('unknown') == 'Carmen' 