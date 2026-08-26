from fastapi import APIRouter, Depends, Query

from movie_to_bear.api.dependencies import get_export_service, get_tmdb_service
from movie_to_bear.models.export import BearExportRequest, BearExportResponse
from movie_to_bear.models.media import MediaSearchResponse
from movie_to_bear.services.export import ExportService
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


@router.get(
    "/search",
    response_model=MediaSearchResponse,
)
async def search(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MediaSearchResponse:
    return await service.search(query)


@router.post(
    "/bear",
    response_model=BearExportResponse,
)
async def export_to_bear(
    request: BearExportRequest,
    service: ExportService = Depends(get_export_service),
) -> BearExportResponse:
    return await service.export_to_bear(
        media_id=request.media_id,
        media_type=request.media_type,
    )
