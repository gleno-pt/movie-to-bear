import httpx

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.core.config import Settings


class AppState:
    def __init__(self, settings: Settings) -> None:
        self.http_client = httpx.AsyncClient(
            base_url="https://api.themoviedb.org/3",
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_token}",
                "accept": "application/json",
            },
        )

        self.tmdb_client = TMDBClient(
            settings=settings,
            http_client=self.http_client,
        )

    async def close(self) -> None:
        await self.http_client.aclose()
