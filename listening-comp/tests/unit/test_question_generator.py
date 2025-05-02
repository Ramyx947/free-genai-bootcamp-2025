import pytest
from question_service.question_generator import QuestionGenerator
from question_service.models import Question

def test_generate_question(question_generator):
    topic = "În România, iarna este foarte frig și ninge des."
    question = question_generator.generate_question(topic)
    
    assert isinstance(question, Question)
    assert len(question.options) == 4
    assert 0 <= question.correct_answer < len(question.options)
    assert question.text.strip() != ""

@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_question_difficulty(question_generator, difficulty):
    topic = "În România, iarna este foarte frig și ninge des."
    question = question_generator.generate_question(
        topic, 
        difficulty=difficulty
    )
    assert question.difficulty is not None 