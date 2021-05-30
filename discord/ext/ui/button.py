from typing import Optional, Union

import discord
from discord import ui
from discord import ButtonStyle, PartialEmoji

from .item import Item
from .utils import _call_any


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
            row: Optional[int] = None,
            callback: Optional[callable] = None
    ):
        super(CustomButton, self).__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row
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
    ):
        self._style = style
        self._label = label
        self._disabled = disabled
        self._url = url
        self._emoji = emoji

        self._row = None

        self.func = None

    def __eq__(self, other: 'Button'):
        return self.to_dict() == other.to_dict()

    def to_discord(self):
        return CustomButton(style=self._style, label=self._label, disabled=self._disabled, url=self._url,
                            emoji=self._emoji, row=self._row, callback=self.func)

    def to_dict(self):
        return {
            'style': self._style,
            'label': self._label,
            'disabled': self._disabled,
            'emoji': self._emoji,
            'row': self._row,
            'callback': id(self.func)
        }

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
