from movie_to_bear.exporters.bear_url import BearURLBuilder
from movie_to_bear.models.bear import BearNote


def test_build_bear_create_url() -> None:
    note = BearNote(
        title="The Matrix",
        text="A computer hacker...",
        tags=["movies", "tmdb"],
    )

    builder = BearURLBuilder()

    result = builder.build(note)

    assert result.startswith("bear://x-callback-url/create?")

    assert "title=The+Matrix" in result
    assert "text=A+computer+hacker..." in result
    assert "tags=movies%2Ctmdb" in result


def test_build_bear_create_url_encodes_special_characters() -> None:
    note = BearNote(
        title="The Matrix: Reloaded & More",
        text="Line one\nLine two",
        tags=["movies", "science fiction"],
    )

    builder = BearURLBuilder()

    result = builder.build(note)

    assert "The+Matrix%3A+Reloaded+%26+More" in result
    assert "Line+one%0ALine+two" in result
    assert "science+fiction" in result
