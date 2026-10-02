from pydantic import BaseModel, ConfigDict, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    secret_key: SecretStr | None = None


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    password: SecretStr


class SecretSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        env_nested_delimiter="__",
        frozen=True,
        extra="ignore",
    )

    api: ApiSettings
    database: DatabaseSettings
