import pytest

from src.app.di.container import create_container
from src.app.settings import AppSettings
from src.app.settings.environment import Environment
from src.core.shared.logging import Logger
from src.core.shared.metrics import HttpMetrics
from src.core.domains.user.service import UserService


@pytest.mark.asyncio
async def test_container_resolves_dependencies() -> None:
    container = create_container(Environment.TEST)

    try:
        settings = await container.get(AppSettings)

        logger = await container.get(Logger)

        metrics = await container.get(HttpMetrics)

        user_service = await container.get(UserService)

        assert settings.environment is Environment.TEST

        assert logger is not None
        assert metrics is not None
        assert user_service is not None

    finally:
        await container.close()


@pytest.mark.asyncio
async def test_app_dependencies_are_singletons() -> None:
    container = create_container(Environment.TEST)

    try:
        logger_1 = await container.get(Logger)
        logger_2 = await container.get(Logger)

        metrics_1 = await container.get(HttpMetrics)
        metrics_2 = await container.get(HttpMetrics)

        assert logger_1 is logger_2
        assert metrics_1 is metrics_2

    finally:
        await container.close()
