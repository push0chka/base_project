from typing import Self
from uuid import uuid4

import pytest

from src.core.entities.user import User
from src.core.services.user import UserService


class FakeLogger:
    def bind(self, **context: object) -> Self:
        return self

    def debug(self, event: str, **context: object) -> None:
        pass

    def info(self, event: str, **context: object) -> None:
        pass

    def warning(self, event: str, **context: object) -> None:
        pass

    def error(self, event: str, **context: object) -> None:
        pass

    def exception(self, event: str, **context: object) -> None:
        pass


class FakeUserRepository:
    def __init__(self, users: list[User] | None = None) -> None:
        self.users = users or []

    async def get_all(self) -> list[User]:
        return list(self.users)


@pytest.mark.asyncio
async def test_get_all_users() -> None:
    expected_users = [
        User(id=uuid4(), name="Ivan"),
        User(id=uuid4(), name="Petr"),
    ]

    repository = FakeUserRepository(users=expected_users)

    service = UserService(repository=repository, logger=FakeLogger())

    users = await service.get_all()

    assert users == expected_users
