from abc import ABC, abstractmethod
from typing import Any, Dict

from fastapi import UploadFile


class FileProcessor(ABC):
    @abstractmethod
    async def process(self, file: UploadFile) -> Dict[str, Any]:
        pass
