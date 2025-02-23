from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from .services.file_processor import process_file
from .services.backend_service import save_vocabulary, get_vocabulary
from .config import Settings
from typing import Dict, Any
import logging
import json
import tempfile
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="Vocab Importer Service",
        description="Microservice for importing vocabulary files",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Global error handler: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        return {"status": "healthy"}

    @app.post("/import")
    async def import_vocabulary(file: UploadFile) -> Dict[str, str]:
        try:
            if file.size > settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="File too large")

            file_ext = file.filename.split('.')[-1].lower()
            if file_ext not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=415, detail="Unsupported file type")

            vocabulary_data = await process_file(file)
            await save_vocabulary(vocabulary_data)
            
            logger.info(f"Successfully imported vocabulary from {file.filename}")
            return {"message": "Vocabulary imported successfully"}
            
        except HTTPException as e:
            logger.warning(f"Import failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Import error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/export")
    async def export_vocabulary() -> FileResponse:
        try:
            # Get vocabulary from backend
            vocabulary_data = await get_vocabulary()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                mode='w+',
                suffix='.json',
                delete=False
            ) as temp_file:
                json.dump(vocabulary_data, temp_file, indent=2)
                
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vocabulary_export_{timestamp}.json"
            
            return FileResponse(
                path=temp_file.name,
                filename=filename,
                media_type='application/json'
            )
            
        except Exception as e:
            logger.error(f"Export error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to export vocabulary"
            )

    return app

app = create_app() 