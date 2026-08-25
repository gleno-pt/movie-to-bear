from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from movie_to_bear.api.routes import router
from movie_to_bear.core.config import settings
from movie_to_bear.core.logging import configure_logging
from movie_to_bear.core.state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict[str, AppState], None]:
    app_state = AppState(settings)

    try:
        yield {
            "app_state": app_state,
        }
    finally:
        await app_state.close()


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

    app.include_router(router)
    return app


app = create_app()
