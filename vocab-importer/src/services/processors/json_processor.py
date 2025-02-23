import json
from .base import FileProcessor
from ...schemas.vocabulary import VocabularyImport

class JsonProcessor(FileProcessor):
    async def process(self, file: UploadFile) -> Dict[str, Any]:
        content = await file.read()
        data = json.loads(content)
        # Validate against schema
        validated_data = VocabularyImport(**data)
        return validated_data.dict() 