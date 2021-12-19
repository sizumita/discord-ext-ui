from __future__ import annotations
from typing import Optional, Callable, Union

import discord
from discord import ui

from .item import Item
from .custom import CustomSelect


class Select(Item):
    def __init__(
            self,
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            options: Optional[list] = None,
            custom_id: Optional[str] = None,
    ) -> None:
        self._placeholder: Optional[str] = placeholder
        self._min_values: int = min_values
        self._max_values: int = max_values
        self._options: list = [] if options is None else options
        self._row: Optional[int] = None
        self._custom_id: Optional[str] = custom_id

        self.func: Optional[Callable] = None
        self.check_func: Optional[Callable[[discord.Interaction], bool]] = None

    def placeholder(self, placeholder: str) -> 'Select':
        self._placeholder = placeholder
        return self

    def min_values(self, min_values: int) -> 'Select':
        self._min_values = min_values
        return self

    def max_values(self, max_values: int) -> 'Select':
        self._max_values = max_values
        return self

    def options(self, options: list[SelectOption]) -> 'Select':
        self._options = [op.to_discord_select_option() for op in options]
        return self

    def row(self, row: int) -> 'Select':
        self._row = row
        return self

    def on_select(self, func: Callable) -> 'Select':
        self.func = func

        return self

    def custom_id(self, custom_id: str) -> 'Select':
        self._custom_id = custom_id
        return self

    def check(self, func: Callable[[discord.Interaction], bool]) -> 'Select':
        self.check_func = func
        return self

    def to_discord_item(self, row: Optional[int]) -> ui.Item:
        return CustomSelect(
            custom_id=self._custom_id,
            placeholder=self._placeholder,
            min_values=self._min_values,
            max_values=self._max_values,
            options=self._options,
            row=row,
            callback=self.func,
            check_func=self.check_func,
        )


class SelectOption:
    def __init__(
            self,
            label: str,
            value: Optional[str] = None,
            description: Optional[str] = None,
            emoji: Optional[Union[str, discord.PartialEmoji]] = None,
            default: bool = False
    ) -> None:
        self._label: str = label
        self._value: Optional[str] = label if value is None else value
        self._description: Optional[str] = description

        if isinstance(emoji, str):
            emoji = discord.PartialEmoji.from_str(emoji)

        self._emoji: Optional[str] = emoji
        self._default: bool = default

    def label(self, label: str) -> 'SelectOption':
        """Set the label of the option.
        The label of the option. This is displayed to users.
        Can only be up to 25 characters.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        label: :class:`str`
            The label to set.
        """
        self._label = label
        return self

    def value(self, value: str) -> 'SelectOption':
        """Set the value of the option.
        The value of the option. This is not displayed to users.
        If not provided when constructed then it defaults to the
        label. Can only be up to 100 characters.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        value: :class:`str`
            The value to set.
        """
        self._value = value
        return self

    def description(self, description: str) -> 'SelectOption':
        """Set the description of the option.
        An additional description of the option.
        Can only be up to 50 characters.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        description: :class:`str`
            The description to set.
        """
        self._description = description
        return self

    def emoji(self, emoji: Optional[Union[str, discord.PartialEmoji]]) -> 'SelectOption':
        """Set the emoji of the option.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        emoji: Optional[Union[:class:`str`, :class:`discord.PartialEmoji`]]
            The description to set.
        """
        if isinstance(emoji, str):
            emoji = discord.PartialEmoji.from_str(emoji)

        self._emoji = emoji
        return self

    def default(self, default: bool) -> 'SelectOption':
        """Set the default of the option.
        Whether this option is selected by default.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        default: :class:`bool`
            The default value to set.
        """
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
