from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_top_players():
    response = client.get("/api/v1/leaderboard/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Test default limit of 10
    assert len(response.json()) <= 10

    # Check response structure
    if len(response.json()) > 0:
        player = response.json()[0]
        assert "rank" in player
        assert "user_email" in player
        assert "endless_score" in player


def test_get_player_ranking():
    # Test with existing user
    test_email = "bao@jie.com"
    response = client.get(f"/api/v1/leaderboard/player/{test_email}")
    assert response.status_code == 200
    player_data = response.json()
    assert "rank" in player_data
    assert "user_email" in player_data
    assert "endless_score" in player_data
    assert player_data["user_email"] == test_email

    # Test with non-existent user
    nonexistent_email = "nonexistent@example.com"
    response = client.get(f"/api/v1/leaderboard/player/{nonexistent_email}")
    assert response.status_code == 404
    assert "Player not found" in response.json()["detail"]


def test_update_player_score():
    # Test updating score for existing user
    user_id = 1
    new_score = 150
    response = client.put(
        f"/api/v1/leaderboard/score/{user_id}?new_score={new_score}")
    assert response.status_code == 200
    assert response.json()["message"] == "Score updated successfully"

    # Verify the score was updated by checking the leaderboard
    response = client.get("/api/v1/leaderboard/top")
    found = False
    for player in response.json():
        if player["endless_score"] == new_score:
            found = True
            break
    assert found

    # Test updating score for non-existent user
    nonexistent_id = 9999
    response = client.put(
        f"/api/v1/leaderboard/score/{nonexistent_id}?new_score=100")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
