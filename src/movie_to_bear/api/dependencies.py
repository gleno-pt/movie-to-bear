from fastapi import Depends

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.core.config import Settings, settings
from movie_to_bear.services.tmdb import TMDBService


def get_settings() -> Settings:
    return settings


def get_tmdb_client(
    app_settings: Settings = Depends(get_settings),
) -> TMDBClient:
    return TMDBClient(app_settings)


def get_tmdb_service(
    client: TMDBClient = Depends(get_tmdb_client),
) -> TMDBService:
    return TMDBService(client)
