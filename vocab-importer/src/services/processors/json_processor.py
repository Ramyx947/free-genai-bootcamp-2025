import json
from typing import Dict, Any
from fastapi import UploadFile
from .base import FileProcessor
from ...schemas.vocabulary import VocabularyImport
from ...errors.exceptions import FileProcessingError

class JSONProcessor(FileProcessor):
    async def process(self, file: UploadFile) -> Dict[str, Any]:
        try:
            content = await file.read()
            data = json.loads(content.decode())
            
            # Validate against schema
            validated_data = VocabularyImport(**data)
            return validated_data.dict()
            
        except json.JSONDecodeError as e:
            raise FileProcessingError(
                f"Invalid JSON format: {str(e)}",
                status_code=400
            )
        except Exception as e:
            raise FileProcessingError(
                f"Error processing JSON file: {str(e)}",
                status_code=422
            ) 