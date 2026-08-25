from movie_to_bear.models.media import Media, MediaType


class BearExporter:
    def export(self, media: Media) -> str:
        lines = [
            f"# {media.title}",
            "",
            f"**Type:** {self._media_type(media)}",
        ]

        if media.release_date:
            lines.append(f"**Release date:** {media.release_date.strftime('%d %B %Y')}")

        lines.extend(
            [
                f"**TMDB ID:** {media.id}",
                "",
            ]
        )

        if media.overview:
            lines.extend(
                [
                    "## Overview",
                    "",
                    media.overview,
                    "",
                ]
            )

        return "\n".join(lines)

    @staticmethod
    def _media_type(media: Media) -> str:
        if media.media_type == MediaType.MOVIE:
            return "Movie"

        return "TV Show"
