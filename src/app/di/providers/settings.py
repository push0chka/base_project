from dishka import Provider, Scope, provide

from src.app.settings import AppSettings
from src.app.settings.environment import Environment
from src.app.settings.settings import load_settings


class SettingsProvider(Provider):
    def __init__(self, environment: Environment) -> None:
        super().__init__(scope=Scope.APP)

        self._environment = environment

    @provide
    def provide_settings(self) -> AppSettings:
        return load_settings(self._environment)
