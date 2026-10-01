from typing import Any

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from pydantic import Field, BaseModel, ConfigDict


class SwaggerConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    js_url: str = "https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"
    css_url: str = "https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
    ui_parameters: dict[str, Any] = Field(
        default_factory=lambda: {"withCredentials": True}
    )


def setup_swagger(
    app: FastAPI, config: SwaggerConfig = SwaggerConfig()
) -> None:
    @app.get("/docs", include_in_schema=False)
    async def swagger_ui():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=config.js_url,
            swagger_css_url=config.css_url,
            swagger_ui_parameters=config.ui_parameters,
        )

    if app.swagger_ui_oauth2_redirect_url:

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()
