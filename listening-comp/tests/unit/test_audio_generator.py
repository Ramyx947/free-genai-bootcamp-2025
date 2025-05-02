import pytest
from audio_service.models import AudioConfig
from audio_service.polly_generator import AudioGenerator

def test_audio_config():
    config = AudioConfig()
    assert config.voice_id == "Carmen"
    assert config.engine == "standard"
    assert config.language_code == "ro-RO"

def test_get_voice_for_gender(audio_generator):
    assert audio_generator.get_voice_for_gender('male') == 'Emil'
    assert audio_generator.get_voice_for_gender('female') == 'Carmen'
    assert audio_generator.get_voice_for_gender('unknown') == 'Carmen'

def test_generate_audio(audio_generator):
    text = "Bună ziua! Acesta este un test."
    audio_file = audio_generator.generate_audio(text)
    assert audio_file is not None
    assert audio_file.endswith('.mp3') 