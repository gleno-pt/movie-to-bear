from unittest.mock import AsyncMock

from movie_to_bear.models.tmdb import MovieSearchResponse
from movie_to_bear.services.tmdb import TMDBService


async def test_search_movies() -> None:
    client = AsyncMock()

    client.search_movies.return_value = {
        "page": 1,
        "results": [
            {
                "id": 603,
                "title": "The Matrix",
                "release_date": "1999-03-30",
                "overview": "A computer hacker learns...",
                "poster_path": "/poster.jpg",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search_movies("The Matrix")

    assert isinstance(result, MovieSearchResponse)
    assert result.page == 1
    assert result.results[0].id == 603
    assert result.results[0].title == "The Matrix"
    assert result.results[0].release_date is not None
    assert result.results[0].release_date.year == 1999

    client.search_movies.assert_awaited_once_with("The Matrix")
