from fastapi import APIRouter, Depends, Query

from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.models.tmdb import MovieSearchResponse
from movie_to_bear.services.tmdb import TMDBService

router = APIRouter(
    prefix="/api/v1",
)


@router.get(
    "/search/movies",
    response_model=MovieSearchResponse,
)
async def search_movies(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MovieSearchResponse:
    return await service.search_movies(query)
