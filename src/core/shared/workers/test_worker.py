import asyncio
from typing import Any

from src.core.shared.workers import Worker


class TestWorker(Worker):
    async def _run(self, *args: Any, **kwargs: Any) -> Any:
        while True:
            await asyncio.sleep(1)

    async def _initialize_logic(self, *args: Any, **kwargs: Any) -> None: ...

    async def _cleanup(self) -> None: ...
