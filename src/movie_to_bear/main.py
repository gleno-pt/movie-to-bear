import structlog
from fastapi import FastAPI

from movie_to_bear.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Movie to Bear",
        version="0.1.0",
    )

    logger = structlog.get_logger()

    @app.get("/health")
    async def health() -> dict[str, str]:
        logger.info(
            "health_check",
            status="ok",
            component="api",
        )

        return {"status": "ok"}

    return app


app = create_app()