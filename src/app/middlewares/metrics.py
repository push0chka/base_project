from __future__ import annotations

import time
from collections.abc import Iterable

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from src.core.metrics import HttpMetrics


class MetricsMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        metrics: HttpMetrics,
        excluded_paths: Iterable[str] = (),
    ) -> None:
        self._app = app
        self._metrics = metrics

        self._excluded_paths = frozenset(
            self._normalize_path(path) for path in excluded_paths
        )

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        path = self._normalize_path(scope["path"])

        if path in self._excluded_paths:
            await self._app(scope, receive, send)
            return

        method = scope["method"]

        status_code = 500

        self._metrics.request_started(method=method)

        started_at = time.perf_counter()

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

            await send(message)

        try:
            await self._app(scope, receive, send_wrapper)
        finally:
            duration = time.perf_counter() - started_at

            route = self._get_route(scope)

            self._metrics.request_finished(
                method=method,
                route=route,
                status_code=status_code,
                duration=duration,
            )

    @staticmethod
    def _normalize_path(path: str) -> str:
        return path.rstrip("/") or "/"

    @staticmethod
    def _get_route(scope: Scope) -> str:
        route = scope.get("route")

        if route is None:
            return "__unmatched__"

        route_path = getattr(route, "path", None)

        if route_path is None:
            return "__unmatched__"

        return route_path
