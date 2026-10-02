from fastapi.testclient import TestClient


def test_request_id_is_generated(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None
    assert request_id


def test_existing_request_id_is_preserved(client: TestClient) -> None:
    request_id = "test-request-123"

    response = client.get("/health", headers={"X-Request-ID": request_id})

    assert response.status_code == 200

    assert response.headers["X-Request-ID"] == request_id
