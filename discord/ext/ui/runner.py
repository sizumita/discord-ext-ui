from typing import Generic, TypeVar, cast, Tuple

import discord

from .abc import Runnable
from .signal import Signal
from .context import Context
from .provider import ContextProvider


S = TypeVar("S", bound=Signal, covariant=True)
P = TypeVar("P", bound=ContextProvider, covariant=True)


class Runner(Generic[P]):
    def __init__(self, provider: P):
        self.provider: P = provider
        self.ctx: Context[P] = Context(self.provider)

    async def run(self, runnable: Runnable[S, P]) -> None:
        await runnable.run(self.ctx)

    async def handle_event(self, name: str, *args) -> None:
        match name:
            case "interaction":
                await self.handle_interaction(cast(Tuple[discord.Interaction], args)[0])

    async def handle_interaction(self, interaction: discord.Interaction):
        # if self.ctx.scope.message_id.check_interaction(interaction):
        #     await self.ctx.scope.present.content
        pass
