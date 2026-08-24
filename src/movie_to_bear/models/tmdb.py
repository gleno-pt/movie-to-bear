from datetime import date

from pydantic import BaseModel


class MovieSearchResult(BaseModel):
    id: int
    title: str
    release_date: date | None = None
    overview: str | None = None
    poster_path: str | None = None


class MovieSearchResponse(BaseModel):
    page: int
    results: list[MovieSearchResult]
    total_pages: int
    total_results: int


class TVSearchResult(BaseModel):
    id: int
    name: str
    first_air_date: date | None = None
    overview: str | None = None
    poster_path: str | None = None


class TVSearchResponse(BaseModel):
    page: int
    results: list[TVSearchResult]
    total_pages: int
    total_results: int
