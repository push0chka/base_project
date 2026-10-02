from dishka import Provider, Scope, alias, provide

from src.app.settings import AppSettings
from src.core.shared.logging import Logger
from src.core.shared.logging.config import LoguruConfig, configure_loguru
from src.core.shared.logging.loguru_logger import LoguruLogger


class LoggingProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_loguru_logger(self, settings: AppSettings) -> LoguruLogger:
        logging_settings = settings.config.logging

        configure_loguru(
            LoguruConfig(
                level=logging_settings.level,
                log_path=logging_settings.path,
                file_name=logging_settings.file_name,
                rotation=logging_settings.rotation,
                retention=logging_settings.retention,
                colorize=logging_settings.colorize,
                enqueue=logging_settings.enqueue,
                disabled_loggers=(logging_settings.disabled_loggers),
            )
        )

        return LoguruLogger()

    logger = alias(source=LoguruLogger, provides=Logger)
