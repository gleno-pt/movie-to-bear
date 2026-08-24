from datetime import date

from fastapi.testclient import TestClient

from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.main import app
from movie_to_bear.models.media import (
    Media,
    MediaSearchResponse,
    MediaType,
)


class FakeTMDBService:
    async def search_movies(self, query: str) -> MediaSearchResponse:
        return MediaSearchResponse(
            page=1,
            results=[
                Media(
                    id=603,
                    media_type=MediaType.MOVIE,
                    title="The Matrix",
                    release_date=date(1999, 3, 30),
                )
            ],
            total_pages=1,
            total_results=1,
        )

    async def search_tv(self, query: str) -> MediaSearchResponse:
        return MediaSearchResponse(
            page=1,
            results=[
                Media(
                    id=1399,
                    media_type=MediaType.TV,
                    title="Game of Thrones",
                    release_date=date(2011, 4, 17),
                )
            ],
            total_pages=1,
            total_results=1,
        )


def test_search_movies() -> None:
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


def test_search_tv() -> None:
    fake_service = FakeTMDBService()

    app.dependency_overrides[get_tmdb_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/search/tv",
            params={"query": "Game of Thrones"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 1
        assert data["results"][0]["id"] == 1399
        assert data["results"][0]["title"] == "Game of Thrones"
        assert data["results"][0]["media_type"] == "tv"

    finally:
        app.dependency_overrides.clear()
