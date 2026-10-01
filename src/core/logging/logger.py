from abc import abstractmethod
from typing import Protocol, Self


class Logger(Protocol):
    @abstractmethod
    def bind(self, **context: object) -> Self: ...

    @abstractmethod
    def debug(self, event: str, **context: object) -> None: ...

    @abstractmethod
    def info(self, event: str, **context: object) -> None: ...

    @abstractmethod
    def warning(self, event: str, **context: object) -> None: ...

    @abstractmethod
    def error(self, event: str, **context: object) -> None: ...

    @abstractmethod
    def exception(self, event: str, **context: object) -> None: ...
