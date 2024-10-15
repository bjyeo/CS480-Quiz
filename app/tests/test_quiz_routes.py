from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_quiz_questions():
    response = client.get("/api/v1/quizzes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_questions_by_subcategory():
    test_subcategory = "SSRF"
    response = client.get(f"/api/v1/quizzes/category/{test_subcategory}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for question in response.json():
        assert question["sub"] == test_subcategory


def test_get_questions_by_nonexistent_subcategory():
    nonexistent_subcategory = "nonexistent_category"
    response = client.get(
        f"/api/v1/quizzes/category/{nonexistent_subcategory}")
    assert response.status_code == 500
    assert "No questions found for subcategory" in response.json()["detail"]
