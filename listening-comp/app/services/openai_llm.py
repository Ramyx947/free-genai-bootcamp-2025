from openai import OpenAI
import logging
from typing import Dict
import os

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        logger.info(f"Initialized OpenAI with model {self.model}")
        
    def generate(self, prompt: str) -> Dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return {"text": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise 