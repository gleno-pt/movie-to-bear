from urllib.parse import urlencode

from movie_to_bear.models.bear import BearNote


class BearURLBuilder:
    BASE_URL = "bear://x-callback-url/create"

    def build(self, note: BearNote) -> str:
        params = {
            "title": note.title,
            "text": note.text,
            "tags": ",".join(note.tags),
        }

        return f"{self.BASE_URL}?{urlencode(params)}"
