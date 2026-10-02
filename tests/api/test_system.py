from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_system_info(client: TestClient) -> None:
    response = client.get("/system-info")

    assert response.status_code == 200

    data = response.json()

    assert "app_version" in data
    assert isinstance(data["app_version"], str)
    assert data["app_version"]
