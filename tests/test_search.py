from datetime import date

from fastapi.testclient import TestClient

from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.main import app
from movie_to_bear.models.tmdb import MovieSearchResponse, MovieSearchResult


def test_search_movies() -> None:
    class FakeTMDBService:
        async def search_movies(self, query: str):
            assert query == "The Matrix"

            return MovieSearchResponse(
                page=1,
                results=[
                    MovieSearchResult(
                        id=603,
                        title="The Matrix",
                        release_date=date(1999, 3, 30),
                        overview="A computer hacker...",
                        poster_path="/poster.jpg",
                    )
                ],
                total_pages=1,
                total_results=1,
            )

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
