from pydantic import BaseModel, Field

from src.app.version import get_app_version


class SystemInfoResponse(BaseModel):
    app_version: str = Field(default_factory=get_app_version)
