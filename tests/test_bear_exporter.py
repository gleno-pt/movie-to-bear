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

    assert result.title == "The Matrix"
    assert result.tags == ["movies"]

    assert "**Type:** Movie" in result.text
    assert "**Release date:** 30 March 1999" in result.text
    assert "**TMDB ID:** 603" in result.text
    assert "https://www.themoviedb.org/movie/603" in result.text
    assert "A computer hacker..." in result.text


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

    assert result.title == "Game of Thrones"
    assert result.tags == ["tv"]

    assert "**Type:** TV Show" in result.text
    assert "https://www.themoviedb.org/tv/1399" in result.text
