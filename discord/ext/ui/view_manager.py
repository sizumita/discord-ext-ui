from typing import Optional
import asyncio

import discord
from discord import ui

from .message import Message
from .types.view_manager import RenderKwargs


class ViewManager:
    def __init__(self) -> None:
        self.message: Optional[Message] = None
        self.discord_message: Optional[discord.Message] = None
        self.view: Optional[ui.View] = None
        self.started: bool = False
        self.update_lock: asyncio.Lock = asyncio.Lock()

    def raise_for_started(self) -> None:
        if not self.started:
            raise Exception("View rendering is not started")

    async def send(self, channel: discord.abc.Messageable, message: Message) -> None:
        if message.component is not None:
            self.view = message.component.make_view()
        self.discord_message = await channel.send(
            content=message.content,
            embed=message.embed,
            view=self.view
        )

    async def start(self, channel: discord.abc.Messageable, message: Message) -> None:
        if self.started:
            raise ValueError("This View has already started")

        await self.send(channel, message)
        self.message = message
        self.started = True

    async def apply(self, apply_message: discord.Message, message: Message) -> None:
        if self.started:
            raise ValueError("This View has already started")

        if message.component is not None:
            self.view = message.component.make_view()

        self.discord_message = apply_message
        await self.discord_message.edit(
            content=message.content,
            embed=message.embed,
            view=self.view
        )
        self.message = message
        self.started = True

    async def update(self, message: Message) -> None:
        self.raise_for_started()
        async with self.update_lock:
            if self.message is None:
                return
            kwargs = await self.message.update(message)
            await self.render(**kwargs)

    async def render(self, **kwargs: RenderKwargs) -> None:
        if self.discord_message is None:
            return
        await self.discord_message.edit(**kwargs)
        self.view = kwargs.get("view", None)
