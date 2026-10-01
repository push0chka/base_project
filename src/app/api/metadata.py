from typing import Any

API_TITLE = "Test API"

API_DESCRIPTION = """Test API description."""

OPENAPI_TAGS: list[dict[str, Any]] = [
    {"name": "users", "description": "User endpoints."}
]
