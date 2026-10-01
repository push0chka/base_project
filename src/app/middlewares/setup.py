from fastapi import FastAPI

from src.core.logging import Logger
from src.core.metrics import HttpMetrics
from src.app.middlewares.metrics import MetricsMiddleware
from src.app.middlewares.request_context import RequestContextMiddleware


def setup_middlewares(
    app: FastAPI, *, logger: Logger, metrics: HttpMetrics
) -> None:
    app.add_middleware(
        MetricsMiddleware, metrics=metrics, excluded_paths={"/metrics"}
    )

    app.add_middleware(RequestContextMiddleware, logger=logger)
