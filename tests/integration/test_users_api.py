from uuid import uuid4

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
            "email": f"invalid-role-{uuid4().hex[:8]}@aegisops.ai",
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

    email = f"integration-test-{uuid4().hex[:8]}@aegisops.ai"

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


def create_test_user(
    token: str,
    *,
    role_id: int = 4,
    organization_id: int | None = 1,
) -> dict:
    email = f"update-test-{uuid4().hex[:12]}@aegisops.ai"

    response = client.post(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": email,
            "full_name": "Update Test User",
            "password": "TestPassword123",
            "role_id": role_id,
            "organization_id": organization_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_admin_can_update_user_full_name():
    token = get_admin_token()

    user = create_test_user(token)

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "full_name": "Updated Test User",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user["id"]
    assert data["full_name"] == "Updated Test User"


def test_admin_can_update_user_email():
    token = get_admin_token()

    user = create_test_user(token)

    new_email = f"updated-{uuid4().hex[:8]}@aegisops.ai"

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": new_email,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == new_email


def test_admin_can_update_user_role_without_full_name():
    token = get_admin_token()

    user = create_test_user(token, role_id=4)

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "role_id": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user["id"]
    assert data["role_id"] == 3


def test_admin_can_update_user_organization():
    token = get_admin_token()

    user = create_test_user(token, organization_id=1)

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "organization_id": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["organization_id"] == 1


def test_admin_can_deactivate_user():
    token = get_admin_token()

    user = create_test_user(token)

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "is_active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["is_active"] is False


def test_admin_cannot_update_user_with_duplicate_email():
    token = get_admin_token()

    first_user = create_test_user(token)
    second_user = create_test_user(token)

    response = client.patch(
        f"/api/v1/users/{second_user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": first_user["email"],
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "A user with this email already exists."
    )


def test_admin_cannot_update_user_with_invalid_role():
    token = get_admin_token()

    user = create_test_user(token)

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "role_id": 9999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found."


def test_admin_cannot_update_user_with_invalid_organization():
    token = get_admin_token()

    user = create_test_user(token)

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "organization_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found."


def test_update_nonexistent_user():
    token = get_admin_token()

    response = client.patch(
        "/api/v1/users/999999",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "full_name": "Nonexistent User",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


def test_update_user_requires_authentication():
    response = client.patch(
        "/api/v1/users/1",
        json={
            "full_name": "Unauthorized Update",
        },
    )

    assert response.status_code == 401