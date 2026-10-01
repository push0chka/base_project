from pathlib import Path

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, YamlConfigSettingsSource

from src.app.settings.config import ConfigSettings
from src.app.settings.environment import Environment
from src.app.settings.secrets import SecretSettings

CONFIG_DIR = Path("config")


class _YamlSettings(BaseSettings): ...


def load_config(environment: Environment) -> ConfigSettings:
    files = [CONFIG_DIR / "base.yml", CONFIG_DIR / f"{environment.value}.yml"]

    source = YamlConfigSettingsSource(
        _YamlSettings,
        yaml_file=files,
        yaml_file_encoding="utf-8",
        deep_merge=True,
    )

    data = source()

    return ConfigSettings.model_validate(data)


class AppSettings(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    environment: Environment
    config: ConfigSettings
    secrets: SecretSettings


def load_settings(environment: Environment) -> AppSettings:
    return AppSettings(
        environment=environment,
        config=load_config(environment),
        secrets=SecretSettings(),
    )
