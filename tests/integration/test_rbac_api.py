from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


USERS = {
    "admin": {
        "email": "admin@aegisops.ai",
        "password": "Admin@12345",
    },
    "executive": {
        "email": "executive@aegisops.ai",
        "password": "Executive@12345",
    },
    "manager": {
        "email": "manager@aegisops.ai",
        "password": "Manager@12345",
    },
    "analyst": {
        "email": "analyst@aegisops.ai",
        "password": "Analyst@12345",
    },
}


def get_token(role: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json=USERS[role],
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(role: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {get_token(role)}",
    }


def test_admin_can_create_organization():
    slug = f"rbac-admin-{uuid4().hex[:12]}"

    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers("admin"),
        json={
            "name": f"RBAC Admin Organization {uuid4().hex[:8]}",
            "slug": slug,
        },
    )

    assert response.status_code == 201


def test_executive_cannot_create_organization():
    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers("executive"),
        json={
            "name": "RBAC Executive Organization",
            "slug": f"rbac-executive-{uuid4().hex[:12]}",
        },
    )

    assert response.status_code == 403


def test_manager_cannot_create_organization():
    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers("manager"),
        json={
            "name": "RBAC Manager Organization",
            "slug": f"rbac-manager-{uuid4().hex[:12]}",
        },
    )

    assert response.status_code == 403


def test_analyst_cannot_create_organization():
    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers("analyst"),
        json={
            "name": "RBAC Analyst Organization",
            "slug": f"rbac-analyst-{uuid4().hex[:12]}",
        },
    )

    assert response.status_code == 403


def test_admin_can_create_user():
    unique_id = uuid4().hex[:12]

    response = client.post(
        "/api/v1/users",
        headers=auth_headers("admin"),
        json={
            "email": f"rbac-admin-{unique_id}@aegisops.ai",
            "full_name": "RBAC Admin Created User",
            "password": "TestUser@12345",
            "role_id": 4,
            "organization_id": 1,
        },
    )

    assert response.status_code == 201


def test_executive_cannot_create_user():
    unique_id = uuid4().hex[:12]

    response = client.post(
        "/api/v1/users",
        headers=auth_headers("executive"),
        json={
            "email": f"rbac-executive-{unique_id}@aegisops.ai",
            "full_name": "RBAC Executive Created User",
            "password": "TestUser@12345",
            "role_id": 4,
            "organization_id": 1,
        },
    )

    assert response.status_code == 403


def test_manager_can_create_user():
    unique_id = uuid4().hex[:12]

    response = client.post(
        "/api/v1/users",
        headers=auth_headers("manager"),
        json={
            "email": f"rbac-manager-{unique_id}@aegisops.ai",
            "full_name": "RBAC Manager Created User",
            "password": "TestUser@12345",
            "role_id": 4,
            "organization_id": 1,
        },
    )

    assert response.status_code == 201


def test_analyst_cannot_create_user():
    unique_id = uuid4().hex[:12]

    response = client.post(
        "/api/v1/users",
        headers=auth_headers("analyst"),
        json={
            "email": f"rbac-analyst-{unique_id}@aegisops.ai",
            "full_name": "RBAC Analyst Created User",
            "password": "TestUser@12345",
            "role_id": 4,
            "organization_id": 1,
        },
    )

    assert response.status_code == 403

def test_admin_can_delete_user():
    unique_id = uuid4().hex[:12]

    create_response = client.post(
        "/api/v1/users",
        headers=auth_headers("admin"),
        json={
            "email": f"rbac-delete-{unique_id}@aegisops.ai",
            "full_name": "RBAC Delete Test User",
            "password": "TestUser@12345",
            "role_id": 4,
            "organization_id": 1,
        },
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/users/{user_id}",
        headers=auth_headers("admin"),
    )

    assert delete_response.status_code == 204


def test_executive_cannot_delete_user():
    response = client.delete(
        "/api/v1/users/2",
        headers=auth_headers("executive"),
    )

    assert response.status_code == 403


def test_manager_cannot_delete_user():
    response = client.delete(
        "/api/v1/users/2",
        headers=auth_headers("manager"),
    )

    assert response.status_code == 403


def test_analyst_cannot_delete_user():
    response = client.delete(
        "/api/v1/users/2",
        headers=auth_headers("analyst"),
    )

    assert response.status_code == 403


def test_delete_user_requires_authentication():
    response = client.delete("/api/v1/users/2")

    assert response.status_code == 401


def test_admin_delete_nonexistent_user():
    response = client.delete(
        "/api/v1/users/999999",
        headers=auth_headers("admin"),
    )

    assert response.status_code == 404