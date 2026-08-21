import httpx
import structlog

from movie_to_bear.core.config import Settings

logger = structlog.get_logger()


class TMDBClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.tmdb_base_url
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_token}",
                "Accept": "application/json",
            },
            timeout=settings.tmdb_timeout,
        )


    async def search_movies(self, query: str) -> dict:
        logger.info(
            "tmdb_search",
            media_type="movie",
            query=query,
        )

        response = await self._client.get(
            "/search/movie",
            params={
                "query": query,
            },
        )

        response.raise_for_status()

        logger.info(
            "tmdb_response",
            media_type="movie",
            status_code=response.status_code,
        )

        return response.json()    
    async def close(self) -> None:
        await self._client.aclose()