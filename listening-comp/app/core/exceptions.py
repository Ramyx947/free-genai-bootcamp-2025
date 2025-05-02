class RomanianLearningException(Exception):
    """Base exception for Romanian Learning app"""
    pass

class TranscriptError(RomanianLearningException):
    """Raised when there's an error processing transcripts"""
    pass

class AudioGenerationError(RomanianLearningException):
    """Raised when there's an error generating audio"""
    pass

class QuestionGenerationError(RomanianLearningException):
    """Raised when there's an error generating questions"""
    pass
