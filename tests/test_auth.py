from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_signup():
    response = client.post(
        f"{settings.API_V1_STR}/signup",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"},
    )
    # Check if user created or already exists
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

def test_login():
    # Ensure user exists first
    client.post(
        f"{settings.API_V1_STR}/signup",
        json={"email": "login_test@example.com", "password": "password123", "full_name": "Login Test"},
    )
    
    login_data = {
        "username": "login_test@example.com",
        "password": "password123"
    }
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"
