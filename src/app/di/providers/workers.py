from collections.abc import Sequence

from dishka import Provider, Scope, collect, provide

from src.core.shared.logging import Logger
from src.core.shared.workers import Worker
from src.core.shared.workers.test_worker import TestWorker


class WorkerProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_some_worker(self, logger: Logger) -> Worker:
        return TestWorker(logger=logger)

    workers = collect(Worker, provides=Sequence[Worker])
