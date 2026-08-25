from fastapi import Depends, Request

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.services.tmdb import TMDBService


def get_tmdb_client(request: Request) -> TMDBClient:
    return request.state.app_state.tmdb_client


def get_tmdb_service(
    client: TMDBClient = Depends(get_tmdb_client),
) -> TMDBService:
    return TMDBService(client)
