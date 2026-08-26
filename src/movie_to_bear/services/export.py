from movie_to_bear.exporters.bear import BearExporter
from movie_to_bear.exporters.bear_url import BearURLBuilder
from movie_to_bear.models.export import BearExportResponse
from movie_to_bear.models.media import MediaType
from movie_to_bear.services.tmdb import TMDBService


class ExportService:
    def __init__(
        self,
        tmdb_service: TMDBService,
        bear_exporter: BearExporter,
        bear_url_builder: BearURLBuilder,
    ) -> None:
        self.tmdb_service = tmdb_service
        self.bear_exporter = bear_exporter
        self.bear_url_builder = bear_url_builder

    async def export_to_bear(
        self,
        media_id: int,
        media_type: MediaType,
    ) -> BearExportResponse:
        media = await self.tmdb_service.get_media(
            media_id,
            media_type,
        )

        note = self.bear_exporter.export(media)

        url = self.bear_url_builder.build(note)

        return BearExportResponse(
            title=note.title,
            url=url,
        )
