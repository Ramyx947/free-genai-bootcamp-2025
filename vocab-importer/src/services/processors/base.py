from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Dict, Any

class FileProcessor(ABC):
    @abstractmethod
    async def process(self, file: UploadFile) -> Dict[str, Any]:
        pass 