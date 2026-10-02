from typing import Protocol

from src.core.domains.user.schemas import User
from src.core.shared.repositories.base import Repository


class UserRepository(Repository[User], Protocol): ...
