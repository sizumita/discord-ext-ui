import abc
import asyncio
import traceback
from typing import TypeVar, Optional

from .context import Context
from .provider import ContextProvider
from .abc import Displayable, Observable, Renderer
from .signal import Signal


S = TypeVar("S", bound=Signal, covariant=True)
P = TypeVar("P", bound=ContextProvider, covariant=True)


class View(Displayable[S, P], Observable, Renderer[P], abc.ABC):
    def __init__(self) -> None:
        self.event_waiter = asyncio.Event()
        self.is_state_updated = False
        self.is_appear = False

    async def appear(self, ctx: Context[P]) -> S:
        # TODO: scopeを次に進める？これはcheckpointでやるべきかもしれない
        msg = await self.render(ctx)

        await ctx.render(msg)

        self.is_appear = True
        event_loop = asyncio.create_task(self._start_event_loop(ctx))
        signal: S = await ctx.scope.signal_queue.get()
        event_loop.cancel()
        if ctx.scope.view is not None:
            ctx.provider.stop_view(ctx.scope.view)

        self.is_appear = False

        return signal

    async def _start_event_loop(self, ctx: Context[P]) -> None:
        try:
            while True:
                await self.event_waiter.wait()

                msg = await self.render(ctx)
                await ctx.render(msg)
                print(self.event_waiter.is_set())
                self.event_waiter.clear()
                print(self.event_waiter.is_set())
                await asyncio.sleep(1)
        except Exception as e:
            traceback.print_exception(e)

    def update(self, name: str):
        if self.is_appear:
            self.event_waiter.set()
