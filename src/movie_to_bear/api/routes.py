from fastapi import APIRouter, Depends, Query

from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.models.media import MediaSearchResponse
from movie_to_bear.services.tmdb import TMDBService

router = APIRouter(
    prefix="/api/v1",
)


@router.get(
    "/search/movies",
    response_model=MediaSearchResponse,
)
async def search_movies(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MediaSearchResponse:
    return await service.search_movies(query)


@router.get(
    "/search/tv",
    response_model=MediaSearchResponse,
)
async def search_tv(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MediaSearchResponse:
    return await service.search_tv(query)
