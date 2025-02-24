import json
import logging
import os
import tempfile
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from openai import AsyncOpenAI

from .config import Settings
from .errors.exceptions import FileProcessingError, VocabImporterError
from .services.backend_service import get_vocabulary, save_vocabulary
from .services.file_processor import process_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize OpenAI client lazily
def get_openai_client():
    if not hasattr(get_openai_client, "_client"):
        get_openai_client._client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return get_openai_client._client


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="Vocab Importer Service",
        description="Microservice for importing vocabulary files",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(f"Global error handler: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        return {"status": "healthy"}

    @app.post("/import", status_code=status.HTTP_201_CREATED)
    async def import_vocabulary(
        file: UploadFile = File(
            default=None,
            description="Vocabulary file to import (.json, .txt, .csv, .pdf)",
        )
    ) -> Dict[str, str]:
        """
        Import vocabulary from file.

        Raises:
            400: Invalid file or format
            413: File too large
            415: Unsupported file type
            422: Processing error
            502: Backend service error
        """
        try:
            # Validate file exists
            if not file:
                raise FileProcessingError(
                    "No file provided", status_code=status.HTTP_400_BAD_REQUEST
                )

            # Validate filename
            if not file.filename:
                raise FileProcessingError(
                    "Invalid file: no filename", status_code=status.HTTP_400_BAD_REQUEST
                )

            # Validate file extension
            file_ext = file.filename.rsplit(".", 1)[-1].lower()
            if file_ext not in settings.ALLOWED_EXTENSIONS:
                raise FileProcessingError(
                    f"Unsupported file type '.{file_ext}'. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}",
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                )

            # Validate content type
            valid_types = {
                "json": "application/json",
                "txt": "text/plain",
                "csv": "text/csv",
                "pdf": "application/pdf",
            }
            if file.content_type not in valid_types.values():
                raise FileProcessingError(
                    f"Invalid content type: {file.content_type}",
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                )

            # Validate file size
            try:
                file_size = 0
                CHUNK_SIZE = 8192  # 8KB chunks

                while chunk := await file.read(CHUNK_SIZE):
                    file_size += len(chunk)
                    if file_size > settings.MAX_FILE_SIZE:
                        raise FileProcessingError(
                            f"File too large. Maximum size is {settings.MAX_FILE_SIZE/1024/1024:.1f}MB",
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        )

                await file.seek(0)  # Reset file pointer

            except Exception as e:
                raise FileProcessingError(
                    f"Error reading file: {str(e)}",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Process file
            try:
                vocabulary_data = await process_file(file)
            except json.JSONDecodeError as e:
                raise FileProcessingError(
                    f"Invalid JSON format: {str(e)}",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                raise FileProcessingError(
                    f"Error processing file: {str(e)}",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            # Save to backend
            try:
                await save_vocabulary(vocabulary_data)
            except Exception as e:
                raise VocabImporterError(
                    f"Error saving to backend: {str(e)}",
                    status_code=status.HTTP_502_BAD_GATEWAY,
                )

            logger.info(f"Successfully imported vocabulary from {file.filename}")
            return {"message": "Vocabulary imported successfully"}

        except (FileProcessingError, VocabImporterError) as e:
            logger.warning(f"Import failed: {str(e)}")
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during import",
            )

    @app.get("/export")
    async def export_vocabulary() -> FileResponse:
        """Export vocabulary as JSON file."""
        temp_file = None
        try:
            # Get vocabulary from backend
            try:
                vocabulary_data = await get_vocabulary()
                if not vocabulary_data:
                    raise VocabImporterError("No data received from backend")
            except VocabImporterError as e:
                raise e
            except Exception as e:
                raise VocabImporterError(
                    f"Error fetching from backend: {str(e)}",
                    status_code=status.HTTP_502_BAD_GATEWAY,
                )

            # Create temporary file
            try:
                temp_file = tempfile.NamedTemporaryFile(
                    mode="w+", suffix=".json", delete=False, encoding="utf-8"
                )

                # Ensure data is serializable
                if not isinstance(vocabulary_data, (dict, list)):
                    raise FileProcessingError(
                        "Invalid data format received from backend",
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                # Write data to file
                json.dump(vocabulary_data, temp_file, indent=2, ensure_ascii=False)
                temp_file.flush()
                os.fsync(temp_file.fileno())  # Ensure data is written to disk
                temp_file.close()

                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"vocabulary_export_{timestamp}.json"

                # Create async cleanup function
                async def cleanup_file():
                    try:
                        if os.path.exists(temp_file.name):
                            os.unlink(temp_file.name)
                    except Exception as e:
                        logger.error(f"Error cleaning up temp file: {e}")

                return FileResponse(
                    path=temp_file.name,
                    filename=filename,
                    media_type="application/json",
                    background=cleanup_file,  # Pass the async function directly
                )

            except Exception as e:
                if temp_file and os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                raise FileProcessingError(
                    f"Error creating export file: {str(e)}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except VocabImporterError as e:
            logger.error(f"Export error: {e.status_code}: {str(e)}")
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected export error: {str(e)}", exc_info=True)
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during export",
            )

    return app


app = create_app()


def generate_vocab_with_openai(prompt=None):
    """Generate vocabulary with OpenAI."""
    try:
        if os.getenv("DEVELOPMENT_MODE") == "true":
            return {
                "groups": [
                    {"group": "Basic Greetings", "words": ["hello", "goodbye"]},
                    {"group": "Numbers", "words": ["one", "two"]},
                ]
            }

        client = get_openai_client()
        if prompt is None:
            prompt = (
                "Generate a list of vocabulary groups for a language learning app. "
                "Each group should have a 'group' key and a 'words' key which is "
                "a list of words. Return the output in valid JSON format."
            )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that generates vocabulary groups.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from OpenAI"}
    except Exception as e:
        return {"error": str(e)}
