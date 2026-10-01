import asyncio
from abc import abstractmethod, ABC
from asyncio import Task
from typing import Any

from src.core.logging.logger import Logger
from src.core.types.errors import IsError


class Worker(ABC):
    """Base class for asynchronous background workers."""

    def __init__(
        self, logger: Logger, name: str = "Worker", restart_delay: float = 1.0
    ) -> None:
        self._name = name

        self._logger = logger.bind(worker=name)

        self._required_init = True
        self._worker_initialize = asyncio.Event()

        self._restart_delay = restart_delay

        self._task: Task[Any] | None = None

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    async def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Worker main logic."""

        raise NotImplementedError

    @abstractmethod
    async def _initialize_logic(self, *args: Any, **kwargs: Any) -> None:
        """Worker initialization logic."""

        raise NotImplementedError

    @abstractmethod
    async def _cleanup(self) -> None:
        """Worker cleanup logic."""

        raise NotImplementedError

    async def initialize(self, *args: Any, **kwargs: Any) -> None:
        self._logger.info("worker.initialization.started")

        await self._initialize_logic(*args, **kwargs)

        self._worker_initialize.set()

        self._logger.info("worker.initialization.completed")

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        while True:
            try:
                if self._required_init:
                    self._worker_initialize.clear()

                    await self.initialize(*args, **kwargs)

                self._logger.info("worker.run.started")

                return await self._run(*args, **kwargs)

            except asyncio.CancelledError:
                self._logger.info("worker.cancelled")
                raise

            except asyncio.TimeoutError:
                self._logger.error("worker.timeout")

            except Exception as exc:
                self._logger.exception(
                    "worker.run.failed",
                    error=str(exc),
                    error_type=type(exc).__name__,
                )

            finally:
                await self.cleanup()

            await asyncio.sleep(self._restart_delay)

    def start(self, *args: Any, **kwargs: Any) -> IsError:
        if self._task is not None and not self._task.done():
            return False, "Task has been already started"

        self._task = asyncio.create_task(
            self.run(*args, **kwargs), name=self._name
        )

        self._logger.info("worker.started", task_name=self._task.get_name())

        return True, ""

    async def stop(self, timeout: float = 10) -> IsError:
        if self._task is None or self._task.done():
            return False, "Inactive task"

        self._logger.info("worker.stopping")

        self._worker_initialize.clear()

        self._task.cancel()

        done, _ = await asyncio.wait([self._task], timeout=timeout)

        if done:
            self._logger.info("worker.stopped")

            return True, ""

        self._logger.warning(
            "worker.stop.timeout",
            task_name=self._task.get_name(),
            timeout=timeout,
        )

        return False, "Couldn't cleanly stop task"

    def done(self) -> bool:
        return self._task is None or self._task.done()

    async def cleanup(self) -> None:
        self._logger.info("worker.cleanup.started")

        try:
            await self._cleanup()

        except Exception as exc:
            self._logger.exception(
                "worker.cleanup.failed",
                error=str(exc),
                error_type=type(exc).__name__,
            )

            return

        self._logger.info("worker.cleanup.completed")
