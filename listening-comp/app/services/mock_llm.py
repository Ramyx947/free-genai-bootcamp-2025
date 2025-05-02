from typing import Dict
import logging

logger = logging.getLogger(__name__)

class MockOpenAIService:
    def __init__(self):
        logger.info("Initializing Mock OpenAI Service")
        
    def generate(self, prompt: str) -> Dict:
        logger.info("Mock OpenAI generating response")
        return {
            "text": """
            Question: Care este capitala României?
            Options:
            A) București
            B) Paris
            C) Berlin
            D) Madrid
            Correct Answer: A
            Explanation: București este capitala României.
            """
        } 