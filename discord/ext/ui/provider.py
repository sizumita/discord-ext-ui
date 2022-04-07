from __future__ import annotations
from typing import Optional

import discord
from discord import ui


class BaseProvider:
    async def send_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        pass

    async def edit_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        pass

    def update_interaction(self, interaction: discord.Interaction):
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


class InteractionProvider(BaseProvider):
    def __init__(self, interaction: discord.Interaction, *args, **kwargs) -> None:
        self.interaction = interaction
        self.message: Optional[discord.Message] = None
        self._args = args
        self._kwargs = kwargs

    async def send_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.Message:
        resp: discord.InteractionResponse = self.interaction.response
        if resp._responded:
            followup: discord.Webhook = self.interaction.followup
            self.message = await followup.send(content, embeds=embeds, view=view, wait=True, *self._args, **self._kwargs)
        else:
            await resp.send_message(content, embeds=embeds, view=view, *self._args, **self._kwargs)
            self.message = await self.interaction.original_message()
        return self.message

    async def edit_message(self, content: Optional[str], embeds: list[discord.Embed], view: ui.View) -> discord.InteractionMessage:
        await self.interaction.edit_original_message(content=content, embeds=embeds, view=view)
        self.message = await self.interaction.original_message()
        return self.message

    def update_interaction(self, interaction: discord.Interaction):
        self.interaction = interaction
