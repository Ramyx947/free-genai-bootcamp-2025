import pytest
import requests
from audio_service.models import TTSRequest

SERVICE_URL = "http://localhost:8003"

@pytest.mark.integration
def test_generate_audio_endpoint():
    request = TTSRequest(
        text="Bună ziua! Acesta este un test.",
        cache_key="test_1"
    )
    
    response = requests.post(
        f"{SERVICE_URL}/generate-audio",
        json=request.dict()
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "audio_data" in data 