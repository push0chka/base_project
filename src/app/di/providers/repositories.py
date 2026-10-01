from dishka import (
    Provider,
    Scope,
    alias,
    provide,
)

from src.core.repositories.user import (
    UserRepository,
)
from src.lib.repositories.memory.user import (
    InMemoryUserRepository,
)


class RepositoryProvider(Provider):
    scope = Scope.APP

    user_repository_impl = provide(
        InMemoryUserRepository,
    )

    user_repository = alias(
        source=InMemoryUserRepository,
        provides=UserRepository,
    )