from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.app.api.docs import setup_swagger
from src.app.api.metadata import API_DESCRIPTION, API_TITLE, OPENAPI_TAGS
from src.app.api.router import router
from src.app.di.container import create_container
from src.app.lifespan import create_lifespan
from src.app.middlewares.setup import setup_middlewares
from src.app.settings.environment import Environment
from src.app.settings import AppSettings
from src.core.shared.logging import Logger
from src.core.shared.metrics import HttpMetrics


def create_app(environment: Environment) -> FastAPI:
    container = create_container(environment)

    settings = container.get_sync(AppSettings)
    logger = container.get_sync(Logger)
    metrics = container.get_sync(HttpMetrics)

    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        openapi_tags=OPENAPI_TAGS,
        docs_url=None,
        redoc_url=None,
        openapi_url=(
            "/openapi.json" if settings.config.server.docs_enabled else None
        ),
        root_path=settings.config.server.root_path,
        lifespan=create_lifespan(container),
    )

    setup_middlewares(app, logger=logger, metrics=metrics)

    app.include_router(router)

    if settings.config.server.docs_enabled:
        setup_swagger(app)

    setup_dishka(container=container, app=app)

    return app
