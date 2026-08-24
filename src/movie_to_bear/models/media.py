from datetime import date
from enum import StrEnum

from pydantic import BaseModel


class MediaType(StrEnum):
    MOVIE = "movie"
    TV = "tv"


class Media(BaseModel):
    id: int
    media_type: MediaType
    title: str
    overview: str | None = None
    release_date: date | None = None
    poster_path: str | None = None


class MediaSearchResponse(BaseModel):
    page: int
    results: list[Media]
    total_pages: int
    total_results: int
