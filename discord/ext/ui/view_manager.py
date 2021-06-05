from typing import Optional
import asyncio

import discord
from discord import ui

from .message import Message


class ViewManager:
    def __init__(self):
        self.message: Optional[Message] = None
        self.discord_message: Optional[discord.Message] = None
        self.view: Optional[ui.View] = None
        self.started: bool = False
        self.update_lock: asyncio.Lock = asyncio.Lock()

    def raise_for_started(self):
        if not self.started:
            raise Exception("View rendering is not started")

    async def send(self, channel: discord.abc.Messageable, message: Message) -> None:
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

        self.view = message.component.make_view()
        self.discord_message = apply_message
        await self.discord_message.edit(
            content=message.content,
            embed=message.embed,
            view=self.view
        )
        self.message = message
        self.started = True

    async def update(self, message: Message):
        self.raise_for_started()
        async with self.update_lock:
            kwargs = await self.message.update(message)
            await self.render(**kwargs)

    async def render(self, **kwargs):
        await self.discord_message.edit(**kwargs)
        self.view = kwargs.get("view", None)
