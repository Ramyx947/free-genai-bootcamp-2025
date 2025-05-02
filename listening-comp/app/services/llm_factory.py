import os
from .mock_llm import MockOpenAIService
from .openai_llm import OpenAIService

def create_llm_service():
    if os.getenv("MOCK_OPENAI", "false").lower() == "true":
        return MockOpenAIService()
    return OpenAIService() 