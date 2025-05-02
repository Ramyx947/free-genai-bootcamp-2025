from youtube_transcript_api import YouTubeTranscriptApi

def test_transcript():
    video_id = "hxrrKINUJcY"
    
    try:
        # Try getting transcript directly
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['ro']  # Try Romanian first
        )
        print("Transcript found!")
        print("\nFirst few lines:")
        for entry in transcript[:3]:
            print(f"Text: {entry['text']}")
            print(f"Start: {entry['start']}")
            print("---")
            
    except Exception as e:
        print(f"Error getting transcript: {str(e)}")
        # Try without language specification
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            print("\nFound transcript in another language:")
            print("Available languages:", YouTubeTranscriptApi.list_transcripts(video_id))
        except Exception as e2:
            print(f"Second error: {str(e2)}")

if __name__ == "__main__":
    test_transcript() 