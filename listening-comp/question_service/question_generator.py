from typing import List
import logging
from models import Question
from services.llm_factory import create_llm_service

# Configure logging
logging.basicConfig(level=logging.DEBUG)
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
        questions = []
        try:
            # Split into question blocks
            blocks = response_text.split("\nQuestion: ")
            
            for block in blocks[1:]:  # Skip first empty block
                lines = block.strip().split("\n")
                
                # Extract question text
                question_text = lines[0].strip()
                
                # Extract options
                options = [
                    line[3:].strip()  # Remove A), B), etc.
                    for line in lines[1:5]
                ]
                
                # Extract correct answer
                correct_line = lines[5]  # "Correct: [A/B/C/D]"
                correct_letter = correct_line.split(": ")[1].strip()
                correct_index = ord(correct_letter) - ord('A')
                
                questions.append(Question(
                    text=question_text,
                    options=options,
                    correct_answer=correct_index
                ))
                
        except Exception as e:
            logger.error(f"Error parsing questions: {str(e)}")
            # Return fallback question
            questions = [
                Question(
                    text="Sample question about the text",
                    options=["Option A", "Option B", "Option C", "Option D"],
                    correct_answer=0
                )
            ]
            
        return questions 