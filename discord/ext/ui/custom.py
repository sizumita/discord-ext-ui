from typing import Optional, Union, Callable

import discord
from discord import ui

from .utils import _call_any


class CustomButton(ui.Button):
    def __init__(
            self,
            label: str = "",
            style: discord.ButtonStyle = discord.ButtonStyle.primary,
            disabled: bool = False,
            emoji: Optional[Union[str, discord.PartialEmoji]] = None,
            custom_id: Optional[str] = None,
    ):
        super().__init__(label=label, style=style, disabled=disabled, emoji=emoji, custom_id=custom_id)
        self.callback_func: Optional[Callable] = None
        self.check_func: Optional[Callable[[discord.Interaction], bool]] = None

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        await _call_any(self.callback_func, interaction)
