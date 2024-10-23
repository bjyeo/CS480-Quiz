from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_quiz():
    subcategory = "SSRF"
    response = client.get(f"/api/v1/generate-quiz/{subcategory}")

    assert response.status_code == 200
    quiz_questions = response.json()

    assert isinstance(quiz_questions, list)
    assert len(quiz_questions) == 15

    for question in quiz_questions:
        assert "question_text" in question
        assert "option_1" in question
        assert "option_2" in question
        assert "option_3" in question
        assert "option_4" in question
        assert "correct_answer" in question
        assert question["sub"] == subcategory

    response2 = client.get(f"/api/v1/generate-quiz/{subcategory}")
    quiz_questions2 = response2.json()
    assert quiz_questions != quiz_questions2, \
        "Two consecutive quizzes should be different"
