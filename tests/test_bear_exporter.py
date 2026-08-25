from datetime import date

from movie_to_bear.exporters.bear import BearExporter
from movie_to_bear.models.media import Media, MediaType


def test_export_movie() -> None:
    media = Media(
        id=603,
        media_type=MediaType.MOVIE,
        title="The Matrix",
        release_date=date(1999, 3, 30),
        overview="A computer hacker...",
    )

    exporter = BearExporter()

    result = exporter.export(media)

    assert "# The Matrix" in result
    assert "#movies" in result
    assert "**Type:** Movie" in result
    assert "**Release date:** 30 March 1999" in result
    assert "**TMDB ID:** 603" in result
    assert "[View on TMDB]" in result
    assert "https://www.themoviedb.org/movie/603" in result


def test_export_tv_show() -> None:
    media = Media(
        id=1399,
        media_type=MediaType.TV,
        title="Game of Thrones",
        release_date=date(2011, 4, 17),
        overview="Seven noble families...",
    )

    exporter = BearExporter()

    result = exporter.export(media)

    assert "# Game of Thrones" in result
    assert "#tv" in result
    assert "**Type:** TV Show" in result
    assert "https://www.themoviedb.org/tv/1399" in result
