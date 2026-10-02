import logging
import sys
from pathlib import Path

from loguru import logger
from pydantic import BaseModel, Field, ConfigDict

LOGGER_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level> | "
    "{extra}"
)


class LoguruConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    level: str = "INFO"

    log_path: Path | None = None
    file_name: str = "app.log"

    rotation: str = "1 day"
    retention: str = "14 days"

    colorize: bool = True
    enqueue: bool = True

    disabled_loggers: tuple[str, ...] = Field(default_factory=tuple)


def configure_loguru(config: LoguruConfig) -> None:
    """Configure application logging."""

    _disable_stdlib_loggers(config.disabled_loggers)

    logger.remove()

    logger.add(
        sys.stderr,
        level=config.level,
        format=LOGGER_FORMAT,
        colorize=config.colorize,
        enqueue=config.enqueue,
    )

    if config.log_path is not None:
        _add_file_sink(config)

    logger.info(
        "Logger configured",
        level=config.level,
        log_path=str(config.log_path) if config.log_path else None,
    )


def _disable_stdlib_loggers(logger_names: tuple[str, ...]) -> None:
    for logger_name in logger_names:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL + 1)


def _add_file_sink(config: LoguruConfig) -> None:
    assert config.log_path is not None

    config.log_path.mkdir(parents=True, exist_ok=True)

    log_file = config.log_path / config.file_name

    logger.add(
        log_file,
        level=config.level,
        format=LOGGER_FORMAT,
        rotation=config.rotation,
        retention=config.retention,
        enqueue=config.enqueue,
        encoding="utf-8",
    )
