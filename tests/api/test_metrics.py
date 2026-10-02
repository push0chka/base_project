from fastapi.testclient import TestClient


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200

    assert "app_http_requests_total" in response.text

    assert "app_http_request_duration_seconds" in response.text

    assert "app_http_requests_in_progress" in response.text


def test_http_request_is_recorded_in_metrics(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200

    metrics_response = client.get("/metrics")

    metrics = metrics_response.text

    assert 'method="GET"' in metrics
    assert 'route="/health"' in metrics
    assert 'status_code="200"' in metrics


def test_metrics_does_not_record_itself(client: TestClient) -> None:
    client.get("/metrics")
    client.get("/metrics")
    client.get("/metrics")

    response = client.get("/metrics")

    assert 'route="/metrics"' not in response.text
