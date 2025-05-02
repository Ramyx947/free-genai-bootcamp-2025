from fastapi import APIRouter, HTTPException
from app.services.aws_polly import PollyGenerator
from app.models.schemas import AudioRequest, AudioResponse
import logging
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)
polly_service = PollyGenerator()

@router.post("/audio", response_model=AudioResponse)
async def generate_audio(request: AudioRequest):
    try:
        audio_path = polly_service.generate_audio(
            text=request.text,
            voice_id=request.voice_id
        )
        
        if not audio_path:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate audio"
            )
            
        return {
            "audio_url": f"/audio/{Path(audio_path).name}",
            "duration": 0  # TODO: Calculate actual duration
        }
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 