from uuid import UUID, uuid4

from src.core.entities.user import User
from src.core.logging.logger import Logger
from src.core.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        self._repository = repository
        self._logger = logger.bind(service="UserService")

    async def create(self, name: str) -> User:
        user = User(id=uuid4(), name=name)

        await self._repository.add(user)

        self._logger.info("user.created", user_id=str(user.id))

        return user

    async def get(self, user_id: UUID) -> User | None:
        return await self._repository.get(user_id)

    async def get_all(self) -> list[User]:
        return await self._repository.get_all()

    async def delete(self, user_id: UUID) -> bool:
        deleted = await self._repository.delete(user_id)

        if deleted:
            self._logger.info("user.deleted", user_id=str(user_id))

        return deleted
