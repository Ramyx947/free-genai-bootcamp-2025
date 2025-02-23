from fastapi import UploadFile, HTTPException
import json
from typing import Dict, Any, List
import logging
from ..schemas.vocabulary import VocabularyImport, VocabularyGroup

logger = logging.getLogger(__name__)

async def process_file(file: UploadFile) -> Dict[str, List[Dict[str, Any]]]:
    """Process uploaded file and return standardized vocabulary format.
    
    Returns:
        Dict with format: {"groups": [{"group": str, "words": List[str]}]}
    
    Raises:
        FileProcessingError: If file processing fails
        JSONDecodeError: If JSON is invalid
    """
    try:
        content = await file.read()
        
        if file.content_type == 'application/json':
            # Parse JSON content
            data = json.loads(content)
            
            # Ensure consistent dictionary structure
            if isinstance(data, list):
                # Convert list to proper format
                data = {"groups": data}
            elif not isinstance(data, dict):
                raise ValueError("Invalid data structure")
            
            # Validate against schema
            validated_data = VocabularyImport(**data)
            return validated_data.dict()
            
        elif file.content_type == 'text/plain':
            # Process text file - one word per line
            words = content.decode().splitlines()
            return {
                "groups": [{
                    "group": "Imported Words",
                    "words": [w.strip() for w in words if w.strip()]
                }]
            }
            
        elif file.content_type == 'text/csv':
            # Process CSV - assume group,word format
            lines = content.decode().splitlines()
            groups = {}
            
            for line in lines[1:]:  # Skip header
                if ',' in line:
                    group, word = line.split(',', 1)
                    groups.setdefault(group.strip(), []).append(word.strip())
            
            return {
                "groups": [
                    {"group": group, "words": words}
                    for group, words in groups.items()
                ]
            }
            
        elif file.content_type == 'application/pdf':
            # TODO: Implement PDF processing
            raise NotImplementedError("PDF processing not yet implemented")
        
        raise HTTPException(
            status_code=415,
            detail=f"Processing {file.content_type} files not implemented"
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"File processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="File processing failed") 