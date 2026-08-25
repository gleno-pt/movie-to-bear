from fastapi.testclient import TestClient

from movie_to_bear.main import app


def test_application_lifespan() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
