from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.models.tmdb import MovieSearchResponse


class TMDBService:
    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def search_movies(
        self,
        query: str,
    ) -> MovieSearchResponse:
        response = await self._client.search_movies(query)

        return MovieSearchResponse.model_validate(response)
