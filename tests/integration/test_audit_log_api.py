from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def token(email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_admin_can_list_audit_logs():
    access_token = token("admin@aegisops.ai", "Admin@12345")
    response = client.get(
        "/api/v1/admin/audit-logs",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert data["count"] >= 1


def test_admin_can_filter_audit_logs_by_action():
    access_token = token("admin@aegisops.ai", "Admin@12345")
    response = client.get(
        "/api/v1/admin/audit-logs",
        params={"action": "LOGIN"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert all(item["action"] == "LOGIN" for item in response.json()["items"])


def test_non_admin_cannot_read_audit_logs():
    access_token = token("executive@aegisops.ai", "Executive@12345")
    response = client.get(
        "/api/v1/admin/audit-logs",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403


def test_audit_log_detail_not_found():
    access_token = token("admin@aegisops.ai", "Admin@12345")
    response = client.get(
        "/api/v1/admin/audit-logs/999999",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
