import httpx
import structlog

from movie_to_bear.core.config import Settings

logger = structlog.get_logger()


class TMDBClient:
    def __init__(
        self,
        settings: Settings,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._http_client = http_client or httpx.AsyncClient(
            base_url=settings.tmdb_base_url,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_token}",
                "Accept": "application/json",
            },
            timeout=settings.tmdb_timeout,
        )

    async def close(self) -> None:
        await self._http_client.aclose()

    async def search_movies(self, query: str) -> dict:
        logger.info(
            "tmdb_search",
            media_type="movie",
            query=query,
        )

        response = await self._http_client.get(
            "/search/movie",
            params={"query": query},
        )

        response.raise_for_status()

        logger.info(
            "tmdb_response",
            media_type="movie",
            status_code=response.status_code,
        )

        return response.json()
