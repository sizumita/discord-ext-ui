import asyncio
from typing import Optional, Union

import discord
from discord import ui
from discord import ButtonStyle, PartialEmoji

from .item import Item


async def _call_any(func, *args, **kwargs):
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


class CustomButton(ui.Button):
    def __init__(
            self,
            *,
            style: ButtonStyle,
            label: str,
            disabled: bool = False,
            custom_id: Optional[str] = None,
            url: Optional[str] = None,
            emoji: Optional[Union[str, PartialEmoji]] = None,
            group: Optional[int] = None,
            callback: Optional[callable] = None
    ):
        super(CustomButton, self).__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            group=group
        )
        self.callback_func = callback

    async def callback(self, interaction: discord.Interaction):
        if self.callback_func is None:
            return
        await _call_any(self.callback_func, interaction)


class Button(Item):
    def __init__(
            self,
            label: str,
            style: ButtonStyle = ButtonStyle.primary,
            disabled: bool = False,
            url: Optional[str] = None,
            emoji: Optional[Union[str, PartialEmoji]] = None,
            group: Optional[int] = None,
    ):
        self._style = style
        self._label = label
        self._disabled = disabled
        self._url = url
        self._emoji = emoji

        self._group = group

        self.func = None

    def to_discord_button(self):
        return CustomButton(
            label=self._label,
            style=self._style,
            disabled=self._disabled,
            url=self._url,
            emoji=self._emoji,
            group=self._group,
            callback=self.func
        )

    def on_click(self, func: callable) -> 'Button':
        self.func = func

        return self

    def style(self, style: discord.ButtonStyle) -> 'Button':
        self._style = style
        return self

    def label(self, label: str) -> 'Button':
        self._label = label
        return self

    def disabled(self, disabled: bool = False) -> 'Button':
        self._disabled = disabled
        return self

    def url(self, url: str) -> 'Button':
        self._url = url
        return self

    def emoji(self, emoji: Union[str, PartialEmoji]) -> 'Button':
        self._emoji = emoji
        return self
