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


def test_admin_can_list_organizations():
    token = get_admin_token()

    response = client.get(
        "/api/v1/organizations",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        organization["slug"] == "aegisops-demo"
        for organization in data
    )


def test_admin_can_get_organization():
    token = get_admin_token()

    response = client.get(
        "/api/v1/organizations/1",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "AegisOps Demo Organization"
    assert data["slug"] == "aegisops-demo"
    assert data["is_active"] is True


def test_admin_can_create_organization():
    token = get_admin_token()

    import uuid

    unique_id = uuid.uuid4().hex[:12]

    name = f"Integration Test Organization {unique_id}"
    slug = f"integration-test-org-{unique_id}"

    response = client.post(
        "/api/v1/organizations",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": name,
            "slug": slug,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == name
    assert data["slug"] == slug
    assert data["is_active"] is True


def test_admin_cannot_create_duplicate_organization():
    token = get_admin_token()

    response = client.post(
        "/api/v1/organizations",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Duplicate Demo Organization",
            "slug": "aegisops-demo",
        },
    )

    assert response.status_code == 409


def test_organizations_endpoint_requires_authentication():
    response = client.get("/api/v1/organizations")

    assert response.status_code == 401


def test_organization_not_found():
    token = get_admin_token()

    response = client.get(
        "/api/v1/organizations/999999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
