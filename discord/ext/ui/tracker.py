from __future__ import annotations
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

    async def track(self, provider: BaseProvider):
        self.body = await self.view.body()
        for item in self.body.get_discord_items():
            self.add_item(item)
        self.message = await provider.send_message(self.body.content_, self.body.embeds_, self)
        self.view._tracker = self
