from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


TEST_EMAIL = "bao@jie.com"
ENGINEERING_DEPT = "Engineering"
OPERATIONS_DEPT = "Operations"


def test_get_top_individuals():
    response = client.get("/api/v1/leaderboard/individual/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert len(response.json()) <= 10

    # Check response structure
    if len(response.json()) > 0:
        player = response.json()[0]
        assert "rank" in player
        assert "user_email" in player
        assert "endless_score" in player
        assert "team_id" in player
        assert "department" in player

        assert player["user_email"] == "vuwet467@gmail.com"
        assert player["endless_score"] == 251


def test_get_individual_ranking():
    response = client.get(
        f"/api/v1/leaderboard/individual/player/{TEST_EMAIL}")
    assert response.status_code == 200
    player_data = response.json()
    assert "rank" in player_data
    assert "user_email" in player_data
    assert "endless_score" in player_data
    assert "team_id" in player_data
    assert "department" in player_data
    assert player_data["user_email"] == TEST_EMAIL
    assert player_data["endless_score"] == 100
    assert player_data["department"] == OPERATIONS_DEPT

    nonexistent_email = "nonexistent@example.com"
    response = client.get(
        f"/api/v1/leaderboard/individual/player/{nonexistent_email}")
    assert response.status_code == 404
    assert "Player not found" in response.json()["detail"]


def test_get_top_teams():
    response = client.get("/api/v1/leaderboard/team/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert len(response.json()) >= 2

    if len(response.json()) > 0:
        team = response.json()[0]
        assert "rank" in team
        assert "team_id" in team
        assert "total_score" in team

        assert team["total_score"] == 401

        team2 = response.json()[1]
        assert team2["total_score"] == 200


def test_get_top_departments():
    response = client.get("/api/v1/leaderboard/department/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert len(response.json()) == 2

    departments = response.json()
    assert departments[0]["department"] == ENGINEERING_DEPT
    assert departments[0]["total_score"] == 401

    assert departments[1]["department"] == OPERATIONS_DEPT
    assert departments[1]["total_score"] == 200


def test_department_aggregation():
    response = client.get("/api/v1/leaderboard/department/top")
    assert response.status_code == 200
    departments = response.json()

    eng_dept = next(
        d for d in departments if d["department"] == ENGINEERING_DEPT)

    response = client.get("/api/v1/leaderboard/individual/top?limit=100")
    dept_users = [p for p in response.json() if p["department"]
                  == ENGINEERING_DEPT]

    calculated_score = sum(user["endless_score"] for user in dept_users)
    assert calculated_score == 401  # 251 + 150
    assert calculated_score == eng_dept["total_score"]


def test_team_aggregation():
    response = client.get("/api/v1/leaderboard/team/top")
    assert response.status_code == 200
    teams = response.json()

    team1 = teams[0]
    team1_id = team1["team_id"]

    response = client.get("/api/v1/leaderboard/individual/top?limit=100")
    team_users = [p for p in response.json() if p.get("team_id") == team1_id]

    calculated_score = sum(user["endless_score"] for user in team_users)
    assert calculated_score == 401  # 251 + 150
    assert calculated_score == team1["total_score"]


def test_update_individual_score():
    user_id = 4
    new_score = 300
    response = client.put(
        f"/api/v1/leaderboard/individual/score/{user_id}?new_score={new_score}")
    assert response.status_code == 200
    assert response.json()["message"] == "Score updated successfully"

    response = client.get("/api/v1/leaderboard/individual/top")
    found = False
    for player in response.json():
        if player["endless_score"] == new_score:
            found = True
            break
    assert found

    response = client.put(
        f"/api/v1/leaderboard/individual/score/{user_id}?new_score=251")
    assert response.status_code == 200

    nonexistent_id = 9999
    response = client.put(
        f"/api/v1/leaderboard/individual/score/{nonexistent_id}?new_score=100")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
