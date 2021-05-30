from typing import Optional, Union

import discord
from discord import PartialEmoji


class SelectOption:
    def __init__(
            self,
            label: str,
            value: Optional[str] = None,
            description: Optional[str] = None,
            emoji: Optional[Union[str, PartialEmoji]] = None,
            default: bool = False,
    ) -> None:
        self._label: str = label
        self._value: Optional[str] = label if value is None else value
        self._description: Optional[str] = description

        if isinstance(emoji, str):
            emoji = PartialEmoji.from_str(emoji)

        self._emoji: Optional[str] = emoji
        self._default: bool = default

    def label(self, label: str) -> 'SelectOption':
        self._label = label
        return self

    def value(self, value: str) -> 'SelectOption':
        self._value = value
        return self

    def description(self, description: str) -> 'SelectOption':
        self._value = description
        return self

    def emoji(self, emoji: Optional[Union[str, PartialEmoji]]) -> 'SelectOption':
        if isinstance(emoji, str):
            emoji = PartialEmoji.from_str(emoji)

        self._emoji = emoji
        return self

    def default(self, default: bool) -> 'SelectOption':
        self._default = default
        return self

    def to_discord_select_option(self) -> discord.SelectOption:
        return discord.SelectOption(
            label=self._label,
            value=self._value,
            description=self._description,
            emoji=self._emoji,
            default=self._default
        )
