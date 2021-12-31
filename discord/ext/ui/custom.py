from __future__ import annotations
from typing import Optional, Union, Callable

import discord
from discord import ui
from discord.utils import MISSING

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


class CustomSelect(ui.Select):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            options: Optional[list[discord.SelectOption]],
            row: Optional[int] = None,
            callback: Optional[Callable] = None,
            check_func: Callable[[discord.Interaction], bool]
    ) -> None:
        custom_id = custom_id or MISSING
        options = options or MISSING
        super(CustomSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func is not None:
            if not self.check_func(interaction):
                return
        selected_options = []
        for label in interaction.data.get("values", []):
            for option in self.options:
                if option.label == label:
                    selected_options.append(option)
                    continue
        await _call_any(self.callback_func, interaction, selected_options)
