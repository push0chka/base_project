from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from fastapi import FastAPI

from src.app.settings import AppSettings
from src.core.logging import Logger
from src.core.workers import Worker


def create_lifespan(container: AsyncContainer):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        settings = await container.get(AppSettings)
        logger = await container.get(Logger)
        workers = await container.get(Sequence[Worker])

        logger.info(
            "application.starting", environment=settings.environment.value
        )

        try:
            for worker in workers:
                success, message = worker.start()

                if not success:
                    logger.error(
                        "worker.start.failed",
                        worker=worker.name,
                        reason=message,
                    )

            logger.info("application.started")

            yield

        finally:
            logger.info("application.stopping")

            for worker in reversed(workers):
                success, message = await worker.stop()

                if not success:
                    logger.warning(
                        "worker.stop.failed",
                        worker=worker.name,
                        reason=message,
                    )

            logger.info("application.stopped")

            await container.close()

    return lifespan
