from typing import Optional, Union, Callable

import discord
from discord import ui
from discord import ButtonStyle, PartialEmoji

from .item import Item
from .utils import _call_any


def _default_check(_: discord.Interaction) -> bool:
    return True


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
            callback: Optional[Callable] = None,
            check_func: Callable[[discord.Interaction], bool]
    ) -> None:
        super(CustomButton, self).__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row
        )
        self.callback_func: Optional[Callable] = callback
        self.check_func: Callable[[discord.Interaction], bool] = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func(interaction):
            await _call_any(self.callback_func, interaction)


class Button(Item):
    def __init__(
            self,
            label: str = "",
            style: ButtonStyle = ButtonStyle.primary,
            disabled: bool = False,
            url: Optional[str] = None,
            emoji: Optional[Union[str, PartialEmoji]] = None,
            custom_id: Optional[str] = None,
    ) -> None:
        self._style: ButtonStyle = style
        self._label: str = label
        self._disabled: bool = disabled
        self._url: Optional[str] = url
        self._emoji: Optional[Union[str, PartialEmoji]] = emoji
        self._custom_id: Optional[str] = custom_id

        self._row: Optional[int] = None

        self.func: Optional[Callable] = None
        self.check_func: Callable[[discord.Interaction], bool] = _default_check

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Button):
            return NotImplemented

        return self.to_dict() == other.to_dict()

    def to_discord(self) -> CustomButton:
        return CustomButton(
            style=self._style,
            label=self._label,
            disabled=self._disabled,
            url=self._url,
            emoji=self._emoji,
            row=self._row,
            callback=self.func,
            custom_id=self._custom_id,
            check_func=self.check_func
        )

    def to_dict(self) -> dict:
        return {
            'style': self._style,
            'label': self._label,
            'disabled': self._disabled,
            'emoji': self._emoji,
            'row': self._row,
            'callback': id(self.func),
            'check': id(self.check_func),
            'custom_id': self._custom_id
        }

    def on_click(self, func: Callable) -> 'Button':
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

    def custom_id(self, custom_id: str) -> 'Button':
        self._custom_id = custom_id
        return self

    def check(self, func: Callable[[discord.Interaction], bool]) -> 'Item':
        self.check_func = func
        return self
