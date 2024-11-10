from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_minigame_endpoint_structure():
    """Test the basic structure and availability of the minigame endpoint"""
    response = client.get("/api/v1/minigame")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "email" in data
    assert "is_modified" in data
    assert "prompt_used" in data
    
    # Check email structure
    email = data["email"]
    assert isinstance(email, dict)
    assert "from" in email
    assert "to" in email
    assert "subject" in email
    assert "content" in email
    
    # Check types
    assert isinstance(data["is_modified"], bool)
    assert isinstance(data["prompt_used"], (str, type(None)))

def test_minigame_prompt_consistency():
    """Test that when is_modified is True, prompt_used exists and vice versa"""
    response = client.get("/api/v1/minigame")
    assert response.status_code == 200
    
    data = response.json()
    if data["is_modified"]:
        assert data["prompt_used"] is not None
        assert isinstance(data["prompt_used"], str)
        assert len(data["prompt_used"]) > 0
    else:
        assert data["prompt_used"] is None