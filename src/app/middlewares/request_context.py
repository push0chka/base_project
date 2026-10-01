import time
from uuid import uuid4

from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from src.core.logging.logger import Logger

REQUEST_ID_HEADER = "X-Request-ID"


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp, logger: Logger) -> None:
        self._app = app
        self._logger = logger.bind(component="http")

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        headers = Headers(scope=scope)

        request_id = headers.get(REQUEST_ID_HEADER) or str(uuid4())

        scope.setdefault("state", {})
        scope["state"]["request_id"] = request_id

        method = scope["method"]
        path = scope["path"]

        client_ip = self._get_client_ip(scope=scope, headers=headers)

        request_logger = self._logger.bind(
            request_id=request_id,
            method=method,
            path=path,
            client_ip=client_ip,
        )

        start_time = time.perf_counter()

        status_code: int | None = None

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

                response_headers = MutableHeaders(scope=message)

                response_headers[REQUEST_ID_HEADER] = request_id

            await send(message)

        try:
            await self._app(scope, receive, send_wrapper)

        except Exception as exc:
            duration = time.perf_counter() - start_time

            request_logger.exception(
                "http.request.failed",
                duration=round(duration, 3),
                error=str(exc),
                error_type=type(exc).__name__,
            )

            raise

        duration = time.perf_counter() - start_time

        request_logger.info(
            "http.request.completed",
            status_code=status_code,
            duration=round(duration, 3),
        )

    @staticmethod
    def _get_client_ip(scope: Scope, headers: Headers) -> str | None:
        forwarded_for = headers.get("x-forwarded-for")

        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        client = scope.get("client")

        if client is None:
            return None

        return client[0]
