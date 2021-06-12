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
        self._value = description
        return self

    def emoji(self, emoji: Optional[Union[str, PartialEmoji]]) -> 'SelectOption':
        """Set the emoji of the option.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        emoji: Optional[Union[:class:`str`, :class:`discord.PartialEmoji`]]
            The description to set.
        """
        if isinstance(emoji, str):
            emoji = PartialEmoji.from_str(emoji)

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
