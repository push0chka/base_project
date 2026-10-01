from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.core.entities.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def get(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_all(self) -> list[User]: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool: ...
