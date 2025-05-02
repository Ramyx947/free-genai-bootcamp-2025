from typing import Dict, List, Optional, Set
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from langdetect import detect, LangDetectException
from urllib.parse import urlparse, parse_qs
import html
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

@dataclass
class VideoGuardrails:
    # Video constraints
    min_duration: int = 60  # Minimum video length in seconds
    max_duration: int = 900  # Maximum video length (15 minutes)
    min_transcript_length: int = 100  # Minimum transcript character length
    max_transcript_length: int = 5000  # Maximum transcript character length
    min_romanian_ratio: float = 0.7  # Minimum ratio of Romanian text
    max_segment_duration: int = 15  # Maximum duration for a single segment
    min_segment_duration: int = 2  # Minimum duration for a single segment
    max_segments: int = 50  # Maximum number of segments per video
    
    # Content constraints
    min_words_per_segment: int = 3  # Minimum words per segment
    max_words_per_segment: int = 50  # Maximum words per segment
    prohibited_words: Set[str] = field(default_factory=lambda: {
        'inappropriate_word1',
        'inappropriate_word2',
        # Add Romanian inappropriate words here
    })
    
    # Rate limiting
    rate_limit: int = 10  # Requests per minute
    daily_limit: int = 100  # Requests per day
    max_concurrent_requests: int = 3  # Maximum concurrent requests per IP
    
    # Channel constraints
    blacklisted_channels: List[str] = field(default_factory=list)
    required_subscriber_count: int = 1000  # Minimum channel subscribers
    min_channel_age_days: int = 30  # Minimum channel age
    
    # Storage constraints
    max_stored_transcripts: int = 1000  # Maximum stored transcripts per user
    max_file_size_mb: int = 10  # Maximum transcript file size in MB
    
    # Request tracking
    requests: Dict[str, List[datetime]] = field(default_factory=dict)
    daily_requests: Dict[str, List[datetime]] = field(default_factory=dict)
    concurrent_requests: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        self.blacklisted_channels = self.blacklisted_channels or []
        self.url_pattern = re.compile(
            r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}$'
        )
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    def validate_url(self, url: str) -> Optional[str]:
        """Validate YouTube URL format and extract video ID."""
        if not self.url_pattern.match(url):
            return "Invalid YouTube URL format"
        
        try:
            parsed_url = urlparse(url)
            if parsed_url.netloc in ['youtube.com', 'www.youtube.com']:
                video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            else:  # youtu.be
                video_id = parsed_url.path[1:]
            
            if not video_id or len(video_id) != 11:
                return "Invalid YouTube video ID"
        except Exception:
            return "Could not parse YouTube URL"
        
        return None

    def check_rate_limit(self, ip_address: str) -> bool:
        """Check if IP has exceeded rate limit"""
        now = datetime.now()
        if ip_address not in self.requests:
            self.requests[ip_address] = []
        
        # Remove old requests
        self.requests[ip_address] = [
            ts for ts in self.requests[ip_address] 
            if now - ts < timedelta(minutes=1)
        ]
        
        if len(self.requests[ip_address]) >= self.rate_limit:
            return False
        
        self.requests[ip_address].append(now)
        return True

    def release_concurrent_request(self, ip_address: str) -> None:
        """Release a concurrent request count for an IP."""
        if ip_address in self.concurrent_requests:
            self.concurrent_requests[ip_address] = max(0, self.concurrent_requests[ip_address] - 1)

    def validate_video_metadata(self, video_id: str) -> Optional[str]:
        """Validate video using YouTube API"""
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            
            if not response["items"]:
                return "Video not found"
                
            video = response["items"][0]
            channel_id = video["snippet"]["channelId"]
            
            # Get channel info
            channel_request = self.youtube.channels().list(
                part="statistics",
                id=channel_id
            )
            channel_response = channel_request.execute()
            
            if not channel_response["items"]:
                return "Channel not found"
                
            subscriber_count = int(channel_response["items"][0]["statistics"]["subscriberCount"])
            
            # Validate metadata
            if subscriber_count < self.required_subscriber_count:
                return f"Channel must have at least {self.required_subscriber_count} subscribers"
                
            return None
            
        except Exception as e:
            return f"Error validating video: {str(e)}"

    def validate_transcript(self, transcript_text: str) -> Optional[str]:
        """Enhanced transcript content validation."""
        if not transcript_text:
            return "Empty transcript"
            
        # Basic length checks
        if len(transcript_text) < self.min_transcript_length:
            return "Transcript is too short."
        
        if len(transcript_text) > self.max_transcript_length:
            return "Transcript is too long."
        
        # Clean and decode HTML entities
        cleaned_text = html.unescape(transcript_text)
        
        # Check for prohibited words
        for word in self.prohibited_words:
            if word.lower() in cleaned_text.lower():
                return "Transcript contains prohibited content."
        
        try:
            # Enhanced Romanian language detection
            chunks = [cleaned_text[i:i+100] for i in range(0, len(cleaned_text), 100)]
            romanian_chunks = 0
            total_valid_chunks = 0
            
            for chunk in chunks:
                if chunk.strip():
                    total_valid_chunks += 1
                    try:
                        if detect(chunk) == 'ro':
                            romanian_chunks += 1
                    except LangDetectException:
                        continue
            
            if total_valid_chunks == 0:
                return "No valid text chunks found."
                
            romanian_ratio = romanian_chunks / total_valid_chunks
            if romanian_ratio < self.min_romanian_ratio:
                return f"Not enough Romanian content detected ({romanian_ratio:.2%})"
            
        except LangDetectException:
            return "Could not verify Romanian language content."
        
        return None

    def validate_segments(self, segments: List[Dict]) -> Optional[str]:
        """Enhanced segment validation."""
        if not segments:
            return "No transcript segments found."
        
        if len(segments) > self.max_segments:
            return f"Too many segments. Maximum allowed is {self.max_segments}."
        
        total_duration = 0
        
        for segment in segments:
            # Duration checks
            duration = segment.get('duration', 0)
            if duration < self.min_segment_duration:
                return f"Segment duration too short ({duration}s)"
            if duration > self.max_segment_duration:
                return f"Segment duration too long ({duration}s)"
            
            total_duration += duration
            
            # Text content checks
            text = segment.get('text', '').strip()
            if not text:
                return "Empty segment detected."
            
            words = text.split()
            if len(words) < self.min_words_per_segment:
                return f"Segment has too few words: {len(words)}"
            if len(words) > self.max_words_per_segment:
                return f"Segment has too many words: {len(words)}"
            
            # Language check
            try:
                if text and detect(text) != 'ro':
                    return "Non-Romanian content detected in segments."
            except LangDetectException:
                continue
        
        # Check total duration
        if total_duration > self.max_duration:
            return f"Total duration exceeds maximum ({total_duration}s)"
        
        return None

    def validate_file_size(self, file_size_bytes: int) -> Optional[str]:
        """Validate file size for storage."""
        max_size_bytes = self.max_file_size_mb * 1024 * 1024
        if file_size_bytes > max_size_bytes:
            return f"File size exceeds maximum of {self.max_file_size_mb}MB"
        return None

    def is_romanian_content(self, text: str) -> bool:
        """Check if content is primarily Romanian"""
        try:
            lang = detect(text)
            return lang == 'ro'
        except:
            # Fallback: check for Romanian characters
            romanian_chars = len(re.findall(r'[ăâîșțĂÂÎȘȚ]', text))
            return romanian_chars > len(text) * 0.1