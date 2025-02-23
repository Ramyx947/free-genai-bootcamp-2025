from fastapi import UploadFile, HTTPException
import json
from typing import Dict, Any, List
import logging
from ..schemas.vocabulary import VocabularyImport, VocabularyGroup
import csv
from io import StringIO

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
            return {
                "groups": [
                    {"group": group, "words": words}
                    for group, words in process_csv_content(content).items()
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

def process_csv_content(content: bytes) -> Dict[str, List[str]]:
    """Process CSV content with proper validation and error handling."""
    lines = content.decode().splitlines()
    if not lines:
        raise ValueError("Empty CSV file")

    groups = {}
    reader = csv.reader(StringIO('\n'.join(lines)))
    
    header = next(reader, None)
    if not header or len(header) != 2 or header != ['group', 'word']:
        raise ValueError("Invalid CSV format. Expected header: group,word")

    for row_num, row in enumerate(reader, start=2):
        if not row:  # Skip empty lines
            continue
        if len(row) != 2:
            raise ValueError(f"Invalid row format at line {row_num}: {','.join(row)}")
        
        group, word = row
        group = group.strip()
        word = word.strip()
        
        if not group or not word:
            raise ValueError(f"Empty group or word at line {row_num}")
            
        groups.setdefault(group, []).append(word)

    return groups 