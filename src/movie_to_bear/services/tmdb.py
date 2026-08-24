from movie_to_bear.clients.tmdb import TMDBClient

class TMDBService:
    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def search_movies(self, query: str) -> dict:
        return await self._client.search_movies(query)