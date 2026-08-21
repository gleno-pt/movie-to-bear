import structlog
from fastapi.testclient import TestClient

from movie_to_bear.main import create_app


def test_health() -> None:
    app = create_app()
    client = TestClient(app)

    with structlog.testing.capture_logs() as logs:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    health_logs = [
        log
        for log in logs
        if log["event"] == "health_check"
    ]

    assert len(health_logs) == 1
    assert health_logs[0]["status"] == "ok"
    assert health_logs[0]["component"] == "api"