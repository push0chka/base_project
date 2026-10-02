from dishka import Provider, Scope, alias, provide

from src.core.domains.user.repo import UserRepository
from src.core.domains.user.in_memory_repo import InMemoryUserRepository


class RepositoryProvider(Provider):
    scope = Scope.APP

    user_repository_impl = provide(InMemoryUserRepository)

    user_repository = alias(
        source=InMemoryUserRepository, provides=UserRepository
    )
