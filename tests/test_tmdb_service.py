from unittest.mock import AsyncMock

from movie_to_bear.models.media import MediaSearchResponse, MediaType
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

    assert isinstance(result, MediaSearchResponse)
    assert result.page == 1
    assert result.results[0].id == 603
    assert result.results[0].title == "The Matrix"
    assert result.results[0].media_type == MediaType.MOVIE
    assert result.results[0].release_date is not None
    assert result.results[0].release_date.year == 1999

    client.search_movies.assert_awaited_once_with("The Matrix")


async def test_search_tv() -> None:
    client = AsyncMock()

    client.search_tv.return_value = {
        "page": 1,
        "results": [
            {
                "id": 1399,
                "name": "Game of Thrones",
                "first_air_date": "2011-04-17",
                "overview": "Seven noble families...",
                "poster_path": "/poster.jpg",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search_tv("Game of Thrones")

    assert isinstance(result, MediaSearchResponse)
    assert result.page == 1

    media = result.results[0]

    assert media.id == 1399
    assert media.title == "Game of Thrones"
    assert media.media_type == MediaType.TV
    assert media.release_date is not None
    assert media.release_date.year == 2011

    client.search_tv.assert_awaited_once_with("Game of Thrones")


async def test_search() -> None:
    client = AsyncMock()

    client.search_movies.return_value = {
        "page": 1,
        "results": [
            {
                "id": 603,
                "title": "The Matrix",
                "release_date": "1999-03-30",
                "overview": "A computer hacker...",
                "poster_path": "/poster.jpg",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    client.search_tv.return_value = {
        "page": 1,
        "results": [
            {
                "id": 1399,
                "name": "Game of Thrones",
                "first_air_date": "2011-04-17",
                "overview": "Seven noble families...",
                "poster_path": "/poster.jpg",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search("test")

    assert result.page == 1
    assert len(result.results) == 2

    assert result.results[0].media_type == MediaType.MOVIE
    assert result.results[0].title == "The Matrix"

    assert result.results[1].media_type == MediaType.TV
    assert result.results[1].title == "Game of Thrones"

    assert result.total_results == 2

    client.search_movies.assert_awaited_once_with("test")
    client.search_tv.assert_awaited_once_with("test")
