import pytest
import requests
from question_service.models import QuestionRequest

SERVICE_URL = "http://localhost:8002"

@pytest.mark.integration
def test_generate_questions_endpoint():
    request = QuestionRequest(
        text="În România, iarna este foarte frig și ninge des.",
        num_questions=2
    )
    
    response = requests.post(
        f"{SERVICE_URL}/generate-questions",
        json=request.dict()
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["questions"]) == 2
    
    # Verify question format
    question = data["questions"][0]
    assert "text" in question
    assert "options" in question
    assert len(question["options"]) == 4
    assert "correct_answer" in question 