import pytest
import requests

SERVICE_URL = "http://localhost:8001"

@pytest.mark.integration
def test_process_video_endpoint():
    video_url = "https://www.youtube.com/watch?v=test_video_id"
    
    response = requests.post(
        f"{SERVICE_URL}/process-video",
        json={"url": video_url}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "segments" in data["data"] 