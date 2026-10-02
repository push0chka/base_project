from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.app.application import create_app
from src.app.settings.environment import Environment


@pytest.fixture
def app() -> FastAPI:
    return create_app(Environment.TEST)


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client
