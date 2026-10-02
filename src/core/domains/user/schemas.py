from uuid import UUID

from pydantic import BaseModel


class UserRawCreateSchema(BaseModel):
    id: UUID
    name: str


class User(BaseModel):
    id: UUID
    name: str
