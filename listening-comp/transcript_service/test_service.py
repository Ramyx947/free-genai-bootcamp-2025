import requests

def test_transcript_processing():
    # Test video ID from URL
    video_id = "hxrrKINUJcY"  # Extracted from https://youtu.be/hxrrKINUJcY
    
    try:
        response = requests.post(
            "http://localhost:8001/process-video",
            json={"video_id": video_id}
        )
        
        print("\nRequest sent successfully!")
        print("\nResponse status:", response.status_code)
        print("\nResponse data:", response.json())
        
    except Exception as e:
        print(f"Error testing service: {str(e)}")

if __name__ == "__main__":
    test_transcript_processing() 