from fastapi import APIRouter, HTTPException
from app.services.question_generator import QuestionGenerator
from app.models.schemas import QuestionRequest, QuestionResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
question_generator = QuestionGenerator()

@router.post("/questions", response_model=QuestionResponse)
async def generate_questions(request: QuestionRequest):
    try:
        questions = question_generator.generate_questions(request.text)
        return QuestionResponse(
            status="success",
            questions=questions
        )
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 