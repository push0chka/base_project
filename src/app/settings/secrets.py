from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecretSettings(BaseSettings):
    secret_key: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )
