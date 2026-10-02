from dishka import Provider, Scope, provide

from src.core.domains.user.service import UserService


class ServiceProvider(Provider):
    scope = Scope.APP

    user_service = provide(UserService)
