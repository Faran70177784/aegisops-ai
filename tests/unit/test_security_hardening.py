from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_security_headers_are_present():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["X-Request-ID"]


def test_client_request_id_is_preserved():
    request_id = "integration-test-request-id"
    response = client.get(
        "/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id
