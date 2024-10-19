from __future__ import annotations
import abc
import asyncio
from typing import Optional, Callable, Awaitable, TypeVar, Generic, Union, cast
from typing_extensions import Self
import os

import discord

from .context import Context
from .error import UnreachableError
from .signal import Signal
from .provider import ContextProvider
from .abc import ViewElement, ViewElementHandler
from .fake import FakeButton, FakeSelect, FakeChannelSelect, FakeRoleSelect, FakeUserSelect, FakeMentionableSelect

S = TypeVar("S", bound=Signal, covariant=True)
P = TypeVar("P", bound=ContextProvider, covariant=True)
ItemT = TypeVar("ItemT", bound=discord.ui.Item)


class Button(Generic[S, P], ViewElement[S, P, discord.ui.Button]):
    def __init__(self, *, label: Optional[str] = None,
                 style: Optional[discord.ButtonStyle] = discord.ButtonStyle.secondary, custom_id: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 emoji: Optional[discord.PartialEmoji | discord.Emoji | str] = None) -> None:
        super().__init__(custom_id)
        self.label = label
        self.style = style
        self.disabled = disabled
        self.emoji = emoji

    def check(self, callback: Callable[[Context, discord.Interaction], bool]) -> Self:
        self.check_function = callback
        return self

    def on_click(self, callback: ViewElementHandler) -> Self:
        self.handler = callback
        return self

    @staticmethod
    def width() -> int:
        return 1

    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.button

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return FakeButton(
            view,
            ctx,
            self.handle,
            style=self.style,
            label=self.label,
            disabled=self.disabled,
            custom_id=self.custom_id,
            emoji=self.emoji,
            row=row
        )

    def __eq__(self, other: Self) -> bool:
        return all([
            self.style == other.style,
            self.label == other.label,
            self.disabled == other.disabled,
            True if self.is_custom_id_random else self.custom_id == other.custom_id,
            self.emoji == other.emoji
        ])


class Link(Generic[S, P], ViewElement[S, P, discord.ui.Button]):
    def __init__(self, *, label: str, url: str) -> None:
        super().__init__(None)
        self.label = label
        self.url = url

    def check(self, callback: Callable[[Context, discord.Interaction], bool]):
        self.check_function = callback

    @staticmethod
    def width() -> int:
        return 1

    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.button

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return discord.ui.Button(
            style=discord.ButtonStyle.link,
            label=self.label,
            url=self.url
        )

    def __eq__(self, other: Self) -> bool:
        return all([
            self.label == other.label,
            self.url == other.url
        ])


class SelectBase(Generic[S, P, ItemT], ViewElement[S, P, ItemT], abc.ABC):
    def __init__(self, *, custom_id: Optional[str] = None, placeholder: Optional[str] = None,
                 min_values: Optional[int] = None, max_values: Optional[int] = None,
                 disabled: Optional[bool] = None) -> None:
        super().__init__(custom_id)
        self._custom_id = custom_id or os.urandom(16).hex()
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def check(self, callback: Callable[[Context, discord.Interaction], bool]) -> Self:
        self.check_function = callback
        return self

    def on_select(self, callback: ViewElementHandler) -> Self:
        self.handler = callback
        return self

    @staticmethod
    def width() -> int:
        return 5


class Select(Generic[S, P], SelectBase[S, P, discord.ui.Select]):
    def __init__(self, *, custom_id: Optional[str] = None, placeholder: Optional[str] = None,
                 min_values: Optional[int] = None, max_values: Optional[int] = None,
                 disabled: Optional[bool] = None) -> None:
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values,
                         max_values=max_values,
                         disabled=disabled)
        self._options: list[discord.SelectOption] = []

    def options(self, options: list[discord.SelectOption]) -> Self:
        self._options = options

        return self

    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.select

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return FakeSelect(
            view,
            ctx,
            self.handle,
            custom_id=self.custom_id,
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
            disabled=self.disabled,
        )

    def __eq__(self, other: Self) -> bool:
        return all([
            True if self.is_custom_id_random else self.custom_id == other.custom_id,
            self.placeholder == other.placeholder,
            self.min_values == other.min_values,
            self.max_values == other.max_values,
            self.disabled == other.disabled,
        ])


class MentionableSelectBase(Generic[S, P, ItemT], SelectBase[S, P, ItemT], abc.ABC):
    def __init__(self, *, custom_id: Optional[str] = None, placeholder: Optional[str] = None,
                 min_values: Optional[int] = None, max_values: Optional[int] = None,
                 disabled: Optional[bool] = None) -> None:
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values,
                         max_values=max_values,
                         disabled=disabled)
        self.default_values: list[discord.abc.Snowflake] = []

    def default(self, default_values: list[discord.abc.Snowflake]) -> Self:
        self.default_values = default_values
        return self


class MentionableSelect(Generic[S, P], MentionableSelectBase[S, P, discord.ui.MentionableSelect]):
    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.mentionable_select

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return FakeMentionableSelect(
            view,
            ctx,
            self.handle,
            custom_id=self.custom_id,
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
            disabled=self.disabled,
            default_values=self.default_values,
        )

    def __eq__(self, other: Self) -> bool:
        return all([
            True if self.is_custom_id_random else self.custom_id == other.custom_id,
            self.placeholder == other.placeholder,
            self.min_values == other.min_values,
            self.max_values == other.max_values,
            self.disabled == other.disabled,
            self.default_values == other.default_values,
        ])


class ChannelSelect(Generic[S, P], MentionableSelectBase[S, P, discord.ui.ChannelSelect]):
    def __init__(self, *, custom_id: Optional[str] = None, placeholder: Optional[str] = None,
                 min_values: Optional[int] = None, max_values: Optional[int] = None,
                 disabled: Optional[bool] = None) -> None:
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values,
                         max_values=max_values,
                         disabled=disabled)
        self._channel_types: list[discord.ChannelType] = []

    def channel_types(self, types: list[discord.ChannelType]) -> Self:
        self._channel_types = types
        return self

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return FakeChannelSelect(
            view,
            ctx,
            self.handle,
            custom_id=self.custom_id,
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
            disabled=self.disabled,
            default_values=self.default_values,
            channel_types=self._channel_types,
        )

    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.channel_select

    def __eq__(self, other: Self) -> bool:
        return all([
            True if self.is_custom_id_random else self.custom_id == other.custom_id,
            self.placeholder == other.placeholder,
            self.min_values == other.min_values,
            self.max_values == other.max_values,
            self.disabled == other.disabled,
            self.default_values == other.default_values,
            self._channel_types == other._channel_types
        ])


class RoleSelect(Generic[S, P], MentionableSelectBase[S, P, discord.ui.RoleSelect]):
    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.role_select

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return FakeRoleSelect(
            view,
            ctx,
            self.handle,
            custom_id=self.custom_id,
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
            disabled=self.disabled,
            default_values=self.default_values,
        )

    def __eq__(self, other: Self) -> bool:
        return all([
            True if self.is_custom_id_random else self.custom_id == other.custom_id,
            self.placeholder == other.placeholder,
            self.min_values == other.min_values,
            self.max_values == other.max_values,
            self.disabled == other.disabled,
            self.default_values == other.default_values
        ])


class UserSelect(Generic[S, P], MentionableSelectBase[S, P, discord.ui.UserSelect]):
    @property
    def type(self) -> discord.ComponentType:
        return discord.ComponentType.user_select

    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        return FakeUserSelect(
            view,
            ctx,
            self.handle,
            custom_id=self.custom_id,
            placeholder=self.placeholder,
            min_values=self.min_values,
            max_values=self.max_values,
            disabled=self.disabled,
            default_values=self.default_values,
        )

    def __eq__(self, other: Self) -> bool:
        return all([
            True if self.is_custom_id_random else self.custom_id == other.custom_id,
            self.placeholder == other.placeholder,
            self.min_values == other.min_values,
            self.max_values == other.max_values,
            self.disabled == other.disabled,
            self.default_values == other.default_values
        ])
