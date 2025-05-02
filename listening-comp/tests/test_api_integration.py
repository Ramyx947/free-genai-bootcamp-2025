import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_audio_generation():
    test_data = {
        "text": "Bună ziua! Cum te simți astăzi?",
        "voice_id": "Carmen"
    }
    response = client.post("/api/audio", json=test_data)
    assert response.status_code == 200
    assert "audio_url" in response.json()

def test_question_generation():
    test_data = {
        "text": "România este o țară în Europa de Est.",
        "num_questions": 1
    }
    response = client.post("/api/questions", json=test_data)
    assert response.status_code == 200
    assert "questions" in response.json()

def test_transcript_processing():
    test_data = {
        "url": "https://www.youtube.com/watch?v=hxrrKINUJcY"
    }
    response = client.post("/api/process-video", json=test_data)
    assert response.status_code == 200
    assert "transcript" in response.json() 