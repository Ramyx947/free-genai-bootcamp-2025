import requests
import json

def test_transcript_processor():
    url = "http://localhost:8001/process-video"
    payload = {
        "url": "https://www.youtube.com/watch?v=your_romanian_video_id"
    }
    response = requests.post(url, json=payload)
    print("Transcript Processor Response:", response.json())

def test_audio_module():
    url = "http://localhost:8003/generate-audio"
    payload = {
        "text": "Bună ziua! Acesta este un test."
    }
    response = requests.post(url, json=payload)
    print("Audio Module Response:", response.json())

if __name__ == "__main__":
    print("Testing Transcript Processor...")
    test_transcript_processor()
    print("\nTesting Audio Module...")
    test_audio_module() 