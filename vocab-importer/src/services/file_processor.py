from fastapi import UploadFile, HTTPException
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

async def process_file(file: UploadFile) -> Dict[str, Any]:
    try:
        content = await file.read()
        if file.content_type == 'application/json':
            return json.loads(content)
        elif file.content_type in ['text/plain', 'text/csv']:
            # Add specific processing for txt/csv files
            pass
        elif file.content_type == 'application/pdf':
            # Add PDF processing
            pass
        
        raise HTTPException(
            status_code=415,
            detail=f"Processing {file.content_type} files not implemented"
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"File processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="File processing failed") 