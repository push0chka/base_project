from pydantic import BaseModel

from src.core.entities.user import User


class CreateUserRequest(BaseModel):
    name: str


class UserResponse(User): ...
