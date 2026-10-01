import asyncio
from uuid import UUID

from src.core.entities.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._storage: dict[UUID, User] = {}
        self._lock = asyncio.Lock()

    async def add(self, user: User) -> None:
        async with self._lock:
            self._storage[user.id] = user

    async def get(self, user_id: UUID) -> User | None:
        async with self._lock:
            return self._storage.get(user_id)

    async def get_all(self) -> list[User]:
        async with self._lock:
            return list(self._storage.values())

    async def delete(self, user_id: UUID) -> bool:
        async with self._lock:
            return self._storage.pop(user_id, None) is not None
