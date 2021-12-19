from __future__ import annotations

import asyncio
from typing import Any, Callable, Optional

from .publisher import Publisher, MapPublisher


async def _call_any(func: Callable, *args: Any, **kwargs: Any) -> Any:
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


class AsyncPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self.child: Optional[AsyncPublisher] = None
        self.parent: Optional[AsyncPublisher] = None
        self.subscribers: list[Callable[[Any], None]] = []

    def chain(self, new_publisher: AsyncPublisher) -> AsyncPublisher:
        new_publisher.parent = self
        self.set_child(new_publisher)
        return new_publisher

    async def downstream(self, value: Any):
        if self.parent is not None:
            await self.parent.downstream(value)

    async def upstream(self, value: Any):
        if self.child is not None:
            await self.child.upstream(value)

        for func in self.subscribers:
            await _call_any(func, value)

    async def dispatch(self) -> Any:
        if self.parent is not None:
            await self.parent.dispatch()

    async def sink(self, func: Callable[[Any], None]) -> AsyncPublisher:
        if self.child is not None:
            await self.child.sink(func)
            return self
        self.subscribers.append(func)
        await self.dispatch()
        return self

    def map(self, func: Callable[[Any], Any]) -> AsyncPublisher:
        if self.child is not None:
            self.child.map(func)
            return self
        new_publisher = AsyncMapPublisher(func)
        self.chain(new_publisher)
        return self


class AsyncMapPublisher(MapPublisher, AsyncPublisher):
    def __init__(self, func: Callable[[Any], Any]) -> None:
        super().__init__(func)
        self.map_func = func

    async def upstream(self, value: Any):
        if isinstance(value, list):
            value = [await _call_any(self.map_func, v) for v in value]
        else:
            value = await _call_any(self.map_func, value)

        for func in self.subscribers:
            await _call_any(func, value)
