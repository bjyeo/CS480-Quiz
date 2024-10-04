from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_quiz():
    subcategory = "SSRF"
    user_id = 1
    response = client.get(f"/api/v1/generate-quiz/{subcategory}?user_id={user_id}")
    
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
        assert question["sub"] == subcategory

def test_generate_quiz_different_users():
    subcategory = "SSRF"
    user_id1 = 1
    user_id2 = 2
    
    response1 = client.get(f"/api/v1/generate-quiz/{subcategory}?user_id={user_id1}")
    response2 = client.get(f"/api/v1/generate-quiz/{subcategory}?user_id={user_id2}")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    quiz1 = response1.json()
    quiz2 = response2.json()
    
    assert quiz1 != quiz2