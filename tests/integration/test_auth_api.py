from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@aegisops.ai",
            "password": "Admin@12345",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_invalid_password():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@aegisops.ai",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_invalid_email():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "does-not-exist@aegisops.ai",
            "password": "Admin@12345",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_current_user_authenticated():
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@aegisops.ai",
            "password": "Admin@12345",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "admin@aegisops.ai"
    assert data["full_name"] == "System Administrator"
    assert data["is_active"] is True
    assert data["role_id"] == 1


def test_current_user_without_token():
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
