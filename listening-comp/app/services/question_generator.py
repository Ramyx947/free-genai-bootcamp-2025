from typing import List
import logging
from app.models.schemas import Question
from app.services.llm_factory import create_llm_service

logger = logging.getLogger(__name__)

class QuestionGenerator:
    def __init__(self):
        try:
            logger.info("Initializing OpenAI service...")
            self.llm = create_llm_service()
            logger.info("OpenAI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI service: {str(e)}")
            raise

    def generate_questions(self, text: str) -> List[Question]:
        prompt = f"""
        Generate a multiple-choice question in Romanian based on this text:
        {text}
        Include 4 options with one correct answer.
        """
        
        try:
            response = self.llm.generate(prompt)
            return self._parse_questions(response["text"])
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return [self._get_fallback_question()]

    def _get_fallback_question(self) -> Question:
        return Question(
            text="Ce înseamnă 'Bună ziua' în engleză?",
            options=[
                "Good morning",
                "Good day",
                "Good evening",
                "Good night"
            ],
            correct_answer=1
        )

    def _parse_questions(self, response_text: str) -> List[Question]:
        # Keep the existing parsing logic
        questions = []
        try:
            blocks = response_text.split("\nQuestion: ")
            for block in blocks[1:]:
                lines = block.strip().split("\n")
                question_text = lines[0].strip()
                options = [line[3:].strip() for line in lines[1:5]]
                correct_line = lines[5]
                correct_letter = correct_line.split(": ")[1].strip()
                correct_index = ord(correct_letter) - ord('A')
                
                questions.append(Question(
                    text=question_text,
                    options=options,
                    correct_answer=correct_index
                ))
        except Exception as e:
            logger.error(f"Error parsing questions: {str(e)}")
            questions = [self._get_fallback_question()]
            
        return questions 