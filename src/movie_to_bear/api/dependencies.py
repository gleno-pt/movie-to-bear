from fastapi import Depends, Request

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.exporters.bear import BearExporter
from movie_to_bear.exporters.bear_url import BearURLBuilder
from movie_to_bear.services.export import ExportService
from movie_to_bear.services.tmdb import TMDBService


def get_tmdb_client(request: Request) -> TMDBClient:
    return request.state.app_state.tmdb_client


def get_tmdb_service(
    client: TMDBClient = Depends(get_tmdb_client),
) -> TMDBService:
    return TMDBService(client)


def get_export_service(
    tmdb_service: TMDBService = Depends(get_tmdb_service),
) -> ExportService:
    return ExportService(
        tmdb_service=tmdb_service,
        bear_exporter=BearExporter(),
        bear_url_builder=BearURLBuilder(),
    )
