from __future__ import annotations

from typing import Optional, Union, Callable, Any

import discord
from discord import ui

from .item import Item
from .custom import CustomButton


class LinkButton(Item):
    def __init__(self, url: str, label: str):
        self.url = url
        self.label = label

    def to_discord_item(self, row: Optional[int]) -> ui.Item:
        button = ui.Button(style=discord.ButtonStyle.link, label=self.label, url=self.url)
        button.row = row
        return button


class Button(Item):
    def __init__(
            self,
            label: str = "",
            style: discord.ButtonStyle = discord.ButtonStyle.primary,
            disabled: bool = False,
            emoji: Optional[Union[str, discord.PartialEmoji]] = None,
            custom_id: Optional[str] = None,
    ):
        self._style: discord.ButtonStyle = style
        self._label: str = label
        self._disabled: bool = disabled
        self._emoji: Optional[Union[str, discord.PartialEmoji]] = emoji
        self._custom_id: Optional[str] = custom_id

        self.callback_func: Optional[Callable[[discord.Interaction], Any]] = None
        self.check_func: Optional[Callable[[discord.Interaction], bool]] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Button):
            return NotImplemented

        return self._label == other._label\
            and self._style == other._style\
            and self._disabled == other._disabled\
            and self._emoji == other._emoji\
            and self._custom_id == other._custom_id

    def style(self, style: discord.ButtonStyle) -> Button:
        self._style = style
        return self

    def label(self, label: str) -> Button:
        self._label = label
        return self

    def disabled(self, disabled: bool = False) -> Button:
        self._disabled = disabled
        return self

    def emoji(self, emoji: Union[str, discord.PartialEmoji]) -> Button:
        self._emoji = emoji
        return self

    def custom_id(self, custom_id: str) -> Button:
        self._custom_id = custom_id
        return self

    def on_click(self, func: Callable[[discord.Interaction], Any]) -> Button:
        self.callback_func = func
        return self

    def check(self, func: Callable[[discord.Interaction], bool]) -> Button:
        self.check_func = func
        return self

    def to_discord_item(self, row: Optional[int]) -> ui.Item:
        button = CustomButton(
            self._label,
            self._style,
            self._disabled,
            self._emoji,
            self._custom_id
        )
        button.check_func = self.check_func
        button.callback_func = self.callback_func
        button.row = row
        return button
