from unittest.mock import AsyncMock, Mock

from movie_to_bear.models.bear import BearNote
from movie_to_bear.models.media import Media, MediaType
from movie_to_bear.services.export import ExportService


async def test_export_to_bear() -> None:
    tmdb_service = AsyncMock()
    bear_exporter = Mock()
    bear_url_builder = Mock()

    media = Media(
        id=603,
        media_type=MediaType.MOVIE,
        title="The Matrix",
    )

    note = BearNote(
        title="The Matrix",
        text="**Type:** Movie",
        tags=["movies"],
    )

    tmdb_service.get_media.return_value = media
    bear_exporter.export.return_value = note
    bear_url_builder.build.return_value = "bear://x-callback-url/create?..."

    service = ExportService(
        tmdb_service=tmdb_service,
        bear_exporter=bear_exporter,
        bear_url_builder=bear_url_builder,
    )

    result = await service.export_to_bear(
        media_id=603,
        media_type=MediaType.MOVIE,
    )

    assert result.title == "The Matrix"
    assert result.url == "bear://x-callback-url/create?..."

    tmdb_service.get_media.assert_awaited_once_with(
        603,
        MediaType.MOVIE,
    )

    bear_exporter.export.assert_called_once_with(media)
    bear_url_builder.build.assert_called_once_with(note)
