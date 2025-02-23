from fastapi import HTTPException

class VocabImporterError(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class FileProcessingError(VocabImporterError):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=422)

class BackendServiceError(VocabImporterError):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=502) 