"""
Transcript Processor Microservice
"""
import sys
import os
from typing import Dict, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import logging
from dotenv import load_dotenv
from googleapiclient.discovery import build
from pytube import YouTube
from services.llm_factory import create_llm_service

from transcript_data import TranscriptData, TranscriptMetadata, TranscriptSegment
from guardrails import VideoGuardrails

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

class TranscriptProcessor:
    def __init__(self):
        self.transcripts_dir = Path("data/romanian_transcripts")
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        self.guardrails = VideoGuardrails()
        
        # Target segment duration (in seconds)
        self.target_segment_duration = 30.0
        
    def segment_transcript(self, transcript_entries: List[Dict]) -> List[TranscriptSegment]:
        """
        Segment transcript into ~30 second chunks, trying to break at natural points
        """
        segments = []
        current_segment = []
        current_duration = 0
        
        for entry in transcript_entries:
            # If adding this entry would exceed target duration
            if current_duration + entry['duration'] > self.target_segment_duration and current_segment:
                # Create segment from accumulated entries
                text = ' '.join(e['text'] for e in current_segment)
                start_time = current_segment[0]['start']
                end_time = current_segment[-1]['start'] + current_segment[-1]['duration']
                
                segments.append(TranscriptSegment(
                    text=text,
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time
                ))
                
                # Reset accumulators
                current_segment = []
                current_duration = 0
            
            # Add entry to current segment
            current_segment.append(entry)
            current_duration += entry['duration']
        
        # Handle any remaining entries
        if current_segment:
            text = ' '.join(e['text'] for e in current_segment)
            start_time = current_segment[0]['start']
            end_time = current_segment[-1]['start'] + current_segment[-1]['duration']
            
            segments.append(TranscriptSegment(
                text=text,
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time
            ))
        
        return segments

    async def process_video(self, video_url: str, ip_address: str) -> TranscriptData:
        """Process video transcript with validation"""
        # Validate URL
        url_error = self.guardrails.validate_url(video_url)
        if url_error:
            raise HTTPException(status_code=400, detail=url_error)
            
        # Check rate limits
        rate_limit_error = self.guardrails.check_rate_limit(ip_address)
        if rate_limit_error:
            raise HTTPException(status_code=429, detail=rate_limit_error)
        
        try:
            # Extract video ID
            video_id = video_url.split("v=")[-1]
            
            # Get video info
            yt = YouTube(video_url)
            logger.info(f"Video title: {yt.title}")
            
            # Get transcript
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=['ro']
                )
                logger.info("Successfully retrieved Romanian transcript")
            except NoTranscriptFound:
                logger.error("No Romanian transcript found")
                raise HTTPException(
                    status_code=404,
                    detail="No Romanian transcript available for this video"
                )
            
            # Get video metadata (you'll need to implement this)
            metadata = self._get_video_metadata(video_id)
            
            # Create transcript metadata
            transcript_metadata = TranscriptMetadata(
                video_id=video_id,
                title=metadata.get('title', ''),
                channel_id=metadata.get('channel_id'),
                channel_name=metadata.get('channel_name'),
                upload_date=metadata.get('upload_date'),
                duration=metadata.get('duration')
            )
            
            # Segment transcript
            segments = self.segment_transcript(transcript_list)
            
            # Create full transcript text
            raw_transcript = ' '.join(seg.text for seg in segments)
            
            # Validate transcript content
            transcript_error = self.guardrails.validate_transcript(raw_transcript)
            if transcript_error:
                raise HTTPException(status_code=400, detail=transcript_error)
            
            # Create TranscriptData object
            transcript_data = TranscriptData(
                metadata=transcript_metadata,
                segments=segments,
                raw_transcript=raw_transcript
            )
            
            # Save to file
            self.save_transcript(transcript_data)
            
            return transcript_data
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.guardrails.release_concurrent_request(ip_address)

    def save_transcript(self, transcript_data: TranscriptData) -> None:
        """Save transcript data as JSON"""
        output_file = self.transcripts_dir / f"{transcript_data.metadata.video_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transcript_data.to_dict(), f, ensure_ascii=False, indent=2)

class TranscriptionService:
    def __init__(self):
        try:
            logger.info("Initializing LLM service...")
            self.llm = create_llm_service()
            self.temp_dir = Path("/tmp/audio")
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            logger.error(f"Failed to initialize TranscriptionService: {str(e)}")
            raise

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio file using OpenAI"""
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            response = self.llm.generate(f"Please transcribe this audio file to Romanian text: {audio_path}")
            logger.info("Transcription completed")
            return response["text"]
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise
        finally:
            # Cleanup temp file
            try:
                os.remove(audio_path)
            except Exception as e:
                logger.warning(f"Error cleaning up temp file: {str(e)}")

class ServiceConfig:
    def __init__(self, name: str, host: str, port: int, endpoint: str):
        self.name = name
        self.host = host
        self.port = port
        self.endpoint = endpoint

# Initialize service configs
question_service = ServiceConfig(
    name="question_service",
    host="question",  # Docker service name
    port=8002,
    endpoint="/generate-questions"
)

# FastAPI app setup
app = FastAPI()
processor = TranscriptProcessor()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

class TranscriptResponse(BaseModel):
    status: str
    transcript: str

# Initialize service
try:
    transcription_service = TranscriptionService()
    logger.info("TranscriptionService initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize TranscriptionService: {str(e)}")
    raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/process-video")
async def process_video(request: VideoRequest) -> TranscriptResponse:
    """Process video and return transcript"""
    try:
        transcript = transcription_service.transcribe_audio(request.url)
        return {
            "status": "success",
            "transcript": transcript
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/video-info/{video_id}")
async def get_video_info(video_id: str):
    try:
        # Get video details using YouTube API
        request = youtube.videos().list(
            part="snippet,contentDetails",
            id=video_id
        )
        response = request.execute()
        
        if not response["items"]:
            raise HTTPException(status_code=404, detail="Video not found")
            
        return response["items"][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/videos")
async def list_videos():
    """List all processed videos"""
    try:
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json')]
        videos = []
        
        for file in files:
            with open(os.path.join(OUTPUT_DIR, file), 'r') as f:
                data = json.load(f)
                videos.append({
                    'video_id': data['video_id'],
                    'title': data['metadata']['title'],
                    'segments_count': len(data['segments'])
                })
        
        return {"success": True, "videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/video/{video_id}")
async def get_video_data(video_id: str):
    """Get processed data for a specific video"""
    try:
        file_path = Path(OUTPUT_DIR) / f"{video_id}.json"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Video not found")
        
        data = json.loads(file_path.read_text(encoding='utf-8'))
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting video {video_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting transcript service...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
