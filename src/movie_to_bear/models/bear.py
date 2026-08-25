from pydantic import BaseModel


class BearNote(BaseModel):
    title: str
    text: str
    tags: list[str]
