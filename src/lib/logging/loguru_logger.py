from collections.abc import Mapping

from loguru import logger as loguru_logger


class LoguruLogger:
    def __init__(self, context: Mapping[str, object] | None = None) -> None:
        self._context = dict(context or {})

    def bind(self, **context: object) -> "LoguruLogger":
        return LoguruLogger(context={**self._context, **context})

    def debug(self, event: str, **context: object) -> None:
        self._log(level="DEBUG", event=event, context=context)

    def info(self, event: str, **context: object) -> None:
        self._log(level="INFO", event=event, context=context)

    def warning(self, event: str, **context: object) -> None:
        self._log(level="WARNING", event=event, context=context)

    def error(self, event: str, **context: object) -> None:
        self._log(level="ERROR", event=event, context=context)

    def exception(self, event: str, **context: object) -> None:
        logger = loguru_logger.bind(**self._context, **context)

        logger.opt(exception=True, depth=1).error(event)

    def _log(
        self, level: str, event: str, context: Mapping[str, object]
    ) -> None:
        logger = loguru_logger.bind(**self._context, **context)

        logger.opt(depth=2).log(level, event)
