from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_quiz():
    subcategory = "SSRF"
    user_email = "test@email.com"
    response = client.get(
        f"/api/v1/generate-quiz/{subcategory}?user_email={user_email}")

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
