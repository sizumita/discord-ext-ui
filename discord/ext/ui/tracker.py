from __future__ import annotations

import asyncio
from typing import Optional

import discord
from discord import ui

from .view import View
from .provider import BaseProvider
from .message import Message


class ViewTracker(ui.View):
    def __init__(self, view: View, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.view: View = view
        self.items: dict[str, str] = {}
        self.body: Optional[Message] = None
        self.message: Optional[discord.Message] = None
        self.provider: Optional[BaseProvider] = None

        self.stop_wait = asyncio.Event()

    async def track(self, provider: BaseProvider):
        self.body = await self.view.body()
        for item in self.body.get_discord_items():
            self.add_item(item)
        self.message = await provider.send_message(self.body.content_, self.body.embeds_, self)
        self.view._tracker = self
        self.provider = provider
        await self.view.on_appear()

    async def update(self):
        body = await self.view.body()
        if self.body != body:
            self.body = body
            self.clear_items()
            for item in self.body.get_discord_items():
                self.add_item(item)
            await self.provider.edit_message(self.body.content_, self.body.embeds_, self)
            await self.view.on_update()