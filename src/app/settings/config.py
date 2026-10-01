from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class LoggingSettings(BaseModel):
    level: str = "INFO"
    to_file: bool = True
    path: Path = Path("logs")
    file_name: str = "app.log"
    rotation: str = "1 day"
    retention: str = "14 days"
    colorize: bool = True
    enqueue: bool = True
    disabled_loggers: tuple[str, ...] = ()

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        value = value.upper()

        allowed_levels = {"TRACE", "DEBUG", "INFO", "WARNING", "ERROR"}

        if value not in allowed_levels:
            raise ValueError(f"Unsupported log level: {value}")

        return value


class ServerSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(default=5000, gt=0, lt=2**16)
    workers: int = Field(default=1, gt=0)
    reload: bool = False
    log_level: str = "INFO"
    root_path: str = ""
    docs_enabled: bool = True
    timezone: str = "Europe/Moscow"


class ConfigSettings(BaseModel):
    logging: LoggingSettings
    server: ServerSettings
