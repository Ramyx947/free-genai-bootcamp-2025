from pydantic import BaseModel
from typing import Optional

class AudioConfig(BaseModel):
    voice_id: str = "Carmen"  # Romanian female voice
    engine: str = "standard"  # Standard engine for Romanian
    language_code: str = "ro-RO"

class TTSRequest(BaseModel):
    text: str
    cache_key: Optional[str] = None

class TTSResponse(BaseModel):
    status: str
    audio_data: str
    message: str
