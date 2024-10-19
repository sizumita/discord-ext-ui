from typing import Any, Callable, Awaitable

from discord import Interaction
from discord._types import ClientT
from typing_extensions import Self

import discord.ui

from .context import Context


class FakeView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    def set_items(self, items: list[discord.ui.Item]):
        self.clear_items()
        for item in items:
            self.add_item(item)


class FakeButton(discord.ui.Button):
    def __init__(self, view: discord.ui.View, context: Context, callback: Callable[[Context, discord.Interaction, discord.ui.Button], Awaitable[None]], **kwargs):
        super().__init__(**kwargs)
        self.context = context

        async def callback2(slf: Self, i: discord.Interaction, data: Any):
            await callback(self.context, i, data)

        self.view_callback = discord.ui.view._ViewCallback(callback2, view, self)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        return await self.view_callback(interaction)


class FakeSelect(discord.ui.Select):
    def __init__(self, view: discord.ui.View, context: Context, callback: Callable[[Context, discord.Interaction, discord.ui.Select], Awaitable[None]], **kwargs):
        self.context = context
        self.callback_fn = callback
        super().__init__(**kwargs)

        async def callback2(slf: Self, i: discord.Interaction, data: Any):
            await slf.callback_fn(self.context, i, data)

        self.view_callback = discord.ui.view._ViewCallback(callback2, view, self)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        return await self.view_callback(interaction)


class FakeMentionableSelect(discord.ui.MentionableSelect):
    def __init__(self, view: discord.ui.View, context: Context, callback: Callable[[Context, discord.Interaction, discord.ui.MentionableSelect], Awaitable[None]], **kwargs):
        self.context = context
        self.callback_fn = callback
        super().__init__(**kwargs)

        async def callback2(slf: Self, i: discord.Interaction, data: Any):
            await slf.callback_fn(self.context, i, data)

        self.view_callback = discord.ui.view._ViewCallback(callback2, view, self)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        return await self.view_callback(interaction)


class FakeUserSelect(discord.ui.UserSelect):
    def __init__(self, view: discord.ui.View, context: Context, callback: Callable[[Context, discord.Interaction, discord.ui.UserSelect], Awaitable[None]], **kwargs):
        self.context = context
        self.callback_fn = callback
        super().__init__(**kwargs)

        async def callback2(slf: Self, i: discord.Interaction, data: Any):
            await slf.callback_fn(self.context, i, data)

        self.view_callback = discord.ui.view._ViewCallback(callback2, view, self)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        return await self.view_callback(interaction)


class FakeRoleSelect(discord.ui.RoleSelect):
    def __init__(self, view: discord.ui.View, context: Context, callback: Callable[[Context, discord.Interaction, discord.ui.RoleSelect], Awaitable[None]], **kwargs):
        self.context = context
        self.callback_fn = callback
        super().__init__(**kwargs)

        async def callback2(slf: Self, i: discord.Interaction, data: Any):
            await slf.callback_fn(self.context, i, data)

        self.view_callback = discord.ui.view._ViewCallback(callback2, view, self)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        return await self.view_callback(interaction)


class FakeChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, view: discord.ui.View, context: Context, callback: Callable[[Context, discord.Interaction, discord.ui.ChannelSelect], Awaitable[None]], **kwargs):
        self.context = context
        self.callback_fn = callback
        super().__init__(**kwargs)

        async def callback2(slf: Self, i: discord.Interaction, data: Any):
            await slf.callback_fn(self.context, i, data)

        self.view_callback = discord.ui.view._ViewCallback(callback2, view, self)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        return await self.view_callback(interaction)
