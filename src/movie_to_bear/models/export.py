from pydantic import BaseModel

from movie_to_bear.models.media import MediaType


class BearExportRequest(BaseModel):
    media_id: int
    media_type: MediaType


class BearExportResponse(BaseModel):
    title: str
    url: str
