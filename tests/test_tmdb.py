from unittest.mock import AsyncMock

import httpx
import pytest

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.core.config import Settings


async def test_search_movies() -> None:
    request = httpx.Request(
        "GET",
        "https://api.themoviedb.org/3/search/movie",
    )

    response = httpx.Response(
        status_code=200,
        request=request,
        json={
            "page": 1,
            "results": [
                {
                    "id": 603,
                    "title": "The Matrix",
                }
            ],
            "total_pages": 1,
            "total_results": 1,
        },
    )

    http_client = AsyncMock(spec=httpx.AsyncClient)
    http_client.get.return_value = response

    settings = Settings(
        tmdb_api_token="test-token",
    )

    client = TMDBClient(
        settings=settings,
        http_client=http_client,
    )

    result = await client.search_movies("The Matrix")

    assert result["page"] == 1
    assert result["results"][0]["id"] == 603
    assert result["results"][0]["title"] == "The Matrix"

    http_client.get.assert_awaited_once_with(
        "/search/movie",
        params={"query": "The Matrix"},
    )


async def test_search_movies_raises_for_http_error() -> None:
    request = httpx.Request(
        "GET",
        "https://api.themoviedb.org/3/search/movie",
    )

    response = httpx.Response(
        status_code=500,
        request=request,
        json={"status_message": "Internal Server Error"},
    )

    http_client = AsyncMock(spec=httpx.AsyncClient)
    http_client.get.return_value = response

    settings = Settings(
        tmdb_api_token="test-token",
    )

    client = TMDBClient(
        settings=settings,
        http_client=http_client,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await client.search_movies("The Matrix")
