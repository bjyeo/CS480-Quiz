from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_score():
    response = client.post("/api/v1/leaderboard/update-score", 
                           json={"user_email": "test@example.com", "score": 100})
    assert response.status_code == 200
    assert response.json()["leaderboard_score"] == 100

def test_get_top_players():
    response = client.get("/api/v1/leaderboard/top-players")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_player_position():
    response = client.get("/api/v1/leaderboard/player-position?email=test@example.com")
    assert response.status_code == 200
    assert "rank" in response.json()

def test_get_department_position():
    response = client.get("/api/v1/leaderboard/department-position?email=test@example.com&department=IT")
    assert response.status_code == 200
    assert "rank" in response.json()

def test_get_team_position():
    response = client.get("/api/v1/leaderboard/team-position?team_id=123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    assert "rank" in response.json()