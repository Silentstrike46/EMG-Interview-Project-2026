from fastapi.testclient import TestClient


def test_health_reports_ok_when_database_is_reachable(client: TestClient) -> None:
    """Test that the health check returns 200 and "ok" when the DB answers."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
