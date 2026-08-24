from fastapi.testclient import TestClient

from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.main import app
from movie_to_bear.models.media import (
    Media,
    MediaSearchResponse,
    MediaType,
)


def test_search_movies() -> None:
    class FakeTMDBService:
        async def search_movies(self, query: str):
            assert query == "The Matrix"

            fake_response = MediaSearchResponse(
                page=1,
                results=[
                    Media(
                        id=603,
                        media_type=MediaType.MOVIE,
                        title="The Matrix",
                        release_date="1999-03-30",
                        overview="A computer hacker...",
                        poster_path="/poster.jpg",
                    )
                ],
                total_pages=1,
                total_results=1,
            )
            return fake_response

    fake_service = FakeTMDBService()
    app.dependency_overrides[get_tmdb_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/search/movies",
            params={"query": "The Matrix"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 1
        assert data["results"][0]["id"] == 603
        assert data["results"][0]["title"] == "The Matrix"

    finally:
        app.dependency_overrides.clear()
