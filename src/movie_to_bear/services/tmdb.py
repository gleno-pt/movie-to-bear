import asyncio

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.models.media import (
    Media,
    MediaSearchResponse,
    MediaType,
)
from movie_to_bear.models.tmdb import (
    MovieSearchResponse,
    TVSearchResponse,
)


class TMDBService:
    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def search_movies(
        self,
        query: str,
    ) -> MediaSearchResponse:
        response = await self._client.search_movies(query)

        tmdb_response = MovieSearchResponse.model_validate(response)

        return MediaSearchResponse(
            page=tmdb_response.page,
            results=[
                Media(
                    id=movie.id,
                    media_type=MediaType.MOVIE,
                    title=movie.title,
                    overview=movie.overview,
                    release_date=movie.release_date,
                    poster_path=movie.poster_path,
                )
                for movie in tmdb_response.results
            ],
            total_pages=tmdb_response.total_pages,
            total_results=tmdb_response.total_results,
        )

    async def search_tv(
        self,
        query: str,
    ) -> MediaSearchResponse:
        response = await self._client.search_tv(query)

        tmdb_response = TVSearchResponse.model_validate(response)

        return MediaSearchResponse(
            page=tmdb_response.page,
            results=[
                Media(
                    id=show.id,
                    media_type=MediaType.TV,
                    title=show.name,
                    overview=show.overview,
                    release_date=show.first_air_date,
                    poster_path=show.poster_path,
                )
                for show in tmdb_response.results
            ],
            total_pages=tmdb_response.total_pages,
            total_results=tmdb_response.total_results,
        )

    async def search(
        self,
        query: str,
    ) -> MediaSearchResponse:
        movie_response, tv_response = await asyncio.gather(
            self.search_movies(query),
            self.search_tv(query),
        )

        return MediaSearchResponse(
            page=1,
            results=[
                *movie_response.results,
                *tv_response.results,
            ],
            total_pages=max(
                movie_response.total_pages,
                tv_response.total_pages,
            ),
            total_results=(movie_response.total_results + tv_response.total_results),
        )

    async def get_movie(self, movie_id: int) -> Media:
        response = await self._client.get_movie(movie_id)
        print("get_movie response:", response)
        return Media(
            id=response["id"],
            media_type=MediaType.MOVIE,
            title=response["title"],
            release_date=response.get("release_date"),
            overview=response.get("overview"),
            poster_path=response.get("poster_path"),
        )

    async def get_tv(self, tv_id: int) -> Media:
        response = await self._client.get_tv(tv_id)

        return Media(
            id=response["id"],
            media_type=MediaType.TV,
            title=response["name"],
            release_date=response.get("first_air_date"),
            overview=response.get("overview"),
            poster_path=response.get("poster_path"),
        )

    async def get_media(
        self,
        media_id: int,
        media_type: MediaType,
    ) -> Media:
        if media_type == MediaType.MOVIE:
            return await self.get_movie(media_id)

        return await self.get_tv(media_id)
