from typing import Protocol


class HttpMetrics(Protocol):
    def request_started(self, method: str) -> None: ...

    def request_finished(
        self, *, method: str, route: str, status_code: int, duration: float
    ) -> None: ...
