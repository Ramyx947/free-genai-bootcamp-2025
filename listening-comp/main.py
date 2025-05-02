from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import audio, questions, transcripts
from app.core.config import Settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load settings
settings = Settings()

# Create FastAPI app
app = FastAPI(
    title="Romanian Learning API",
    description="API for Romanian language learning features",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(audio.router, prefix="/api", tags=["audio"])
app.include_router(questions.router, prefix="/api", tags=["questions"])
app.include_router(transcripts.router, prefix="/api", tags=["transcripts"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 