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
