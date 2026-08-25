from movie_to_bear.models.bear import BearNote
from movie_to_bear.models.media import Media, MediaType


class BearExporter:
    def export(self, media: Media) -> BearNote:
        lines = [
            f"**Type:** {self._media_type(media)}",
            "",
        ]

        if media.release_date:
            lines.append(f"**Release date:** {media.release_date.strftime('%d %B %Y')}")

        lines.extend(
            [
                f"**TMDB ID:** {media.id}",
                f"[View on TMDB]({media.tmdb_url})",
                "",
            ]
        )

        if media.overview:
            lines.extend(
                [
                    "## Overview",
                    "",
                    media.overview,
                ]
            )

        return BearNote(
            title=media.title,
            text="\n".join(lines),
            tags=[self._tag(media)],
        )

    @staticmethod
    def _media_type(media: Media) -> str:
        if media.media_type == MediaType.MOVIE:
            return "Movie"

        return "TV Show"

    @staticmethod
    def _tag(media: Media) -> str:
        if media.media_type == MediaType.MOVIE:
            return "movies"

        return "tv"
