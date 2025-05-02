from fastapi import APIRouter, HTTPException
from app.services.transcript_processor import TranscriptProcessor
from app.models.schemas import VideoRequest
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
transcript_processor = TranscriptProcessor()

@router.post("/process-video")
async def process_video(request: VideoRequest):
    try:
        transcript_data = transcript_processor.process_video(request.url)
        return {
            "transcript": transcript_data.raw_transcript,
            "segments": [segment.dict() for segment in transcript_data.segments]
        }
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 