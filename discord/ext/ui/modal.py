from __future__ import annotations

from discord import ui
import discord

from typing import List, Callable, Any
from .utils import _call_any


class Modal(ui.Modal):
    def __init__(self, title: str, components: List[ui.TextInput]):
        super().__init__(title=title)
        for component in components:
            self.add_item(component)

        self._hook = None

    def hook(self, func: Callable[[discord.Interaction], Any]) -> Modal:
        self._hook = func
        return self

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self._hook is not None:
            await _call_any(self._hook, interaction)
        if not interaction.response.is_done():
            await interaction.response.defer()
