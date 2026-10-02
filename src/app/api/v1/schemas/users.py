from pydantic import BaseModel

from src.core.domains.user.schemas import User


class CreateUserRequest(BaseModel):
    name: str


class UserResponse(User): ...
