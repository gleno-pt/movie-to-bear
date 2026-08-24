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
