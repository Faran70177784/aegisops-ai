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


def auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {get_admin_token()}",
    }


def create_test_organization() -> tuple[int, str, str]:
    unique_id = uuid4().hex[:12]

    name = f"Integration Test Organization {unique_id}"
    slug = f"integration-test-org-{unique_id}"

    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers(),
        json={
            "name": name,
            "slug": slug,
            "description": "Integration test organization.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    return data["id"], name, slug


def test_admin_can_list_organizations():
    response = client.get(
        "/api/v1/organizations",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        organization["slug"] == "aegisops-demo"
        for organization in data
    )


def test_admin_can_get_organization():
    response = client.get(
        "/api/v1/organizations/1",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "AegisOps Demo Organization"
    assert data["slug"] == "aegisops-demo"
    assert data["is_active"] is True


def test_admin_can_create_organization():
    unique_id = uuid4().hex[:12]

    name = f"Integration Test Organization {unique_id}"
    slug = f"integration-test-org-{unique_id}"

    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers(),
        json={
            "name": name,
            "slug": slug,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == name
    assert data["slug"] == slug
    assert data["description"] is None
    assert data["is_active"] is True


def test_admin_cannot_create_duplicate_organization():
    response = client.post(
        "/api/v1/organizations",
        headers=auth_headers(),
        json={
            "name": "Duplicate Demo Organization",
            "slug": "aegisops-demo",
        },
    )

    assert response.status_code == 409


def test_admin_cannot_create_duplicate_organization_name():
    unique_id = uuid4().hex[:12]

    name = f"Duplicate Name Organization {unique_id}"
    slug = f"duplicate-name-org-{unique_id}"

    first_response = client.post(
        "/api/v1/organizations",
        headers=auth_headers(),
        json={
            "name": name,
            "slug": slug,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/organizations",
        headers=auth_headers(),
        json={
            "name": name,
            "slug": f"another-slug-{unique_id}",
        },
    )

    assert second_response.status_code == 409


def test_admin_can_update_organization_name():
    organization_id, _, slug = create_test_organization()

    new_name = f"Updated Organization {uuid4().hex[:12]}"

    response = client.patch(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
        json={
            "name": new_name,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["name"] == new_name
    assert data["slug"] == slug


def test_admin_can_update_organization_slug():
    organization_id, name, _ = create_test_organization()

    new_slug = f"updated-org-{uuid4().hex[:12]}"

    response = client.patch(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
        json={
            "slug": new_slug,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["name"] == name
    assert data["slug"] == new_slug


def test_admin_can_update_organization_description():
    organization_id, _, _ = create_test_organization()

    description = "Updated organization description."

    response = client.patch(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
        json={
            "description": description,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["description"] == description


def test_admin_can_update_organization_active_status():
    organization_id, _, _ = create_test_organization()

    response = client.patch(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
        json={
            "is_active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["is_active"] is False


def test_admin_can_update_multiple_organization_fields():
    organization_id, _, _ = create_test_organization()

    unique_id = uuid4().hex[:12]

    new_name = f"Fully Updated Organization {unique_id}"
    new_slug = f"fully-updated-org-{unique_id}"
    new_description = "Fully updated organization."

    response = client.patch(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
        json={
            "name": new_name,
            "slug": new_slug,
            "description": new_description,
            "is_active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == organization_id
    assert data["name"] == new_name
    assert data["slug"] == new_slug
    assert data["description"] == new_description
    assert data["is_active"] is False


def test_admin_cannot_update_organization_with_duplicate_name():
    existing_id, existing_name, _ = create_test_organization()
    target_id, _, _ = create_test_organization()

    assert existing_id != target_id

    response = client.patch(
        f"/api/v1/organizations/{target_id}",
        headers=auth_headers(),
        json={
            "name": existing_name,
        },
    )

    assert response.status_code == 409


def test_admin_cannot_update_organization_with_duplicate_slug():
    existing_id, _, existing_slug = create_test_organization()
    target_id, _, _ = create_test_organization()

    assert existing_id != target_id

    response = client.patch(
        f"/api/v1/organizations/{target_id}",
        headers=auth_headers(),
        json={
            "slug": existing_slug,
        },
    )

    assert response.status_code == 409


def test_update_nonexistent_organization():
    response = client.patch(
        "/api/v1/organizations/999999",
        headers=auth_headers(),
        json={
            "name": "Nonexistent Organization",
        },
    )

    assert response.status_code == 404


def test_update_organization_requires_authentication():
    response = client.patch(
        "/api/v1/organizations/1",
        json={
            "name": "Unauthorized Organization",
        },
    )

    assert response.status_code == 401


def test_admin_can_delete_organization():
    organization_id, _, _ = create_test_organization()

    response = client.delete(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/organizations/{organization_id}",
        headers=auth_headers(),
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_organization():
    response = client.delete(
        "/api/v1/organizations/999999",
        headers=auth_headers(),
    )

    assert response.status_code == 404


def test_delete_organization_requires_authentication():
    response = client.delete(
        "/api/v1/organizations/1",
    )

    assert response.status_code == 401


def test_organizations_endpoint_requires_authentication():
    response = client.get("/api/v1/organizations")

    assert response.status_code == 401


def test_organization_not_found():
    response = client.get(
        "/api/v1/organizations/999999",
        headers=auth_headers(),
    )

    assert response.status_code == 404