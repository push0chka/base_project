from dishka import AsyncContainer, make_async_container

from src.app.di.providers.logging import LoggingProvider
from src.app.di.providers.metrics import MetricsProvider
from src.app.di.providers.repositories import RepositoryProvider
from src.app.di.providers.services import ServiceProvider
from src.app.di.providers.settings import SettingsProvider
from src.app.di.providers.workers import WorkerProvider
from src.app.settings.environment import Environment


def create_container(environment: Environment) -> AsyncContainer:
    return make_async_container(
        SettingsProvider(environment),
        LoggingProvider(),
        MetricsProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        WorkerProvider(),
    )
