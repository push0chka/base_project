from uuid import UUID

from src.core.domains.user.schemas import User
from src.core.domains.user.repo import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._storage: dict[UUID, User] = {}

    async def add(self, user: User) -> None:
        self._storage[user.id] = user

    async def get(self, user_id: UUID) -> User | None:
        return self._storage.get(user_id)

    async def get_all(self) -> list[User]:
        return list(self._storage.values())

    async def delete(self, user_id: UUID) -> bool:
        return self._storage.pop(user_id, None) is not None
