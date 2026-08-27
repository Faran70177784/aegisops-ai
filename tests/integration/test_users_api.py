from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def get_admin_token() -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@aegisops.ai",
            "password": "Admin@12345",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_admin_can_list_users():
    token = get_admin_token()

    response = client.get(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        user["email"] == "admin@aegisops.ai"
        for user in data
    )


def test_admin_can_get_user():
    token = get_admin_token()

    response = client.get(
        "/api/v1/users/1",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "admin@aegisops.ai"
    assert data["full_name"] == "System Administrator"
    assert data["role_id"] == 1


def test_admin_cannot_create_duplicate_user():
    token = get_admin_token()

    response = client.post(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "admin@aegisops.ai",
            "full_name": "Duplicate Administrator",
            "password": "Admin@12345",
            "role_id": 4,
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "A user with this email already exists."
    )


def test_admin_create_user_with_invalid_role():
    token = get_admin_token()

    response = client.post(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "invalid-role-test@aegisops.ai",
            "full_name": "Invalid Role Test",
            "password": "TestPassword123",
            "role_id": 9999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found."


def test_users_endpoint_requires_authentication():
    response = client.get("/api/v1/users")

    assert response.status_code == 401


def test_admin_can_create_user():
    token = get_admin_token()

    email = "integration-test-user@aegisops.ai"

    # Remove the test user first if a previous test run left it behind.
    from backend.app.db.database import SessionLocal
    from backend.app.models.user import User

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user is not None:
            db.delete(existing_user)
            db.commit()
    finally:
        db.close()

    response = client.post(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "Integration Test User",
            "password": "TestPassword123",
            "role_id": 4,
            "organization_id": 1,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["full_name"] == "Integration Test User"
    assert data["role_id"] == 4
    assert data["organization_id"] == 1
    assert data["is_active"] is True

