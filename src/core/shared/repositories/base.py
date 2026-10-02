from typing import Protocol, TypeVar
from uuid import UUID

T = TypeVar("T")


class Repository(Protocol[T]):
    async def add(self, entity: T) -> None: ...

    async def get(self, entity_id: UUID) -> T | None: ...

    async def get_all(self) -> list[T]: ...

    async def delete(self, entity_id: UUID) -> bool: ...
