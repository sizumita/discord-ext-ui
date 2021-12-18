from __future__ import annotations
from typing import Optional

import discord
from discord import ui


class BaseProvider:
    async def send_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        pass

    async def edit_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        pass


class MessageProvider(BaseProvider):
    def __init__(self, channel: discord.TextChannel) -> None:
        self.channel = channel
        self.message: Optional[discord.Message] = None

    async def send_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        self.message = await self.channel.send(content, embeds=embeds, view=view)
        return self.message

    async def edit_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        await self.message.edit(content=content, embeds=embeds, view=view)
        return self.message
