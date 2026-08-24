from unittest.mock import AsyncMock

from movie_to_bear.services.tmdb import TMDBService


async def test_search_movies() -> None:
    client = AsyncMock()

    client.search_movies.return_value = {
        "page": 1,
        "results": [
            {
                "id": 603,
                "title": "The Matrix",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search_movies("The Matrix")

    assert result["page"] == 1
    assert result["results"][0]["id"] == 603
    assert result["results"][0]["title"] == "The Matrix"

    client.search_movies.assert_awaited_once_with("The Matrix")