from fastapi.testclient import TestClient


def test_get_users_returns_empty_list(client: TestClient) -> None:
    response = client.get("/api/v1/users")

    assert response.status_code == 200
    assert response.json() == []


def test_create_user(client: TestClient) -> None:
    response = client.post("/api/v1/users/user", json={"name": "Ivan"})

    assert response.status_code in {200, 201}

    data = response.json()

    assert data["name"] == "Ivan"
    assert "id" in data


def test_created_user_is_returned_by_get_users(client: TestClient) -> None:
    create_response = client.post("/api/v1/users/user", json={"name": "Ivan"})

    assert create_response.status_code in {200, 201}

    created_user = create_response.json()

    response = client.get("/api/v1/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1

    assert users[0]["id"] == created_user["id"]
    assert users[0]["name"] == "Ivan"


def test_create_user_without_name_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/users/user", json={})

    assert response.status_code == 422
