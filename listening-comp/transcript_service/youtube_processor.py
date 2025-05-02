from typing import Dict, List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from .models import TranscriptSegment, TranscriptMetadata
from .guardrails import VideoGuardrails
from pytube import YouTube
import logging

logger = logging.getLogger(__name__)

class YouTubeProcessor:
    def __init__(self):
        self.guardrails = VideoGuardrails()
        self.target_segment_duration = 30.0  # Target duration in seconds

    def get_transcript(self, video_id: str) -> List[Dict]:
        """Get transcript from YouTube video"""
        try:
            return YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['ro']  # Try Romanian first
            )
        except Exception as e:
            raise Exception(f"Failed to get transcript: {str(e)}")

    def segment_transcript(self, structured_transcript: List[Dict], segment_duration: int = 30) -> List[Dict]:
        """Segment transcript into fixed duration chunks"""
        segments = []
        current_segment = []
        current_duration = 0
        segment_start = 0
        
        for entry in structured_transcript:
            if current_duration == 0:
                segment_start = entry['start']
            
            current_segment.append(entry)
            current_duration += entry['duration']
            
            if current_duration >= segment_duration:
                segment_text = ' '.join([e['text'] for e in current_segment])
                segments.append({
                    'start': segment_start,
                    'end': segment_start + current_duration,
                    'duration': current_duration,
                    'text': segment_text
                })
                current_segment = []
                current_duration = 0
        
        return segments

    def get_video_metadata(self, video_id: str) -> Dict:
        """Enhanced metadata retrieval using pytube"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            yt = YouTube(url)
            return {
                'title': yt.title,
                'author': yt.author,
                'description': yt.description,
                'length': yt.length,
                'publish_date': str(yt.publish_date),
                'views': yt.views
            }
        except Exception as e:
            logger.error(f"Error getting metadata: {str(e)}")
            return None
