from typing import Optional
import asyncio

import discord
from discord import ui

from .message import Message
from .types.view import Target
from .types.view_manager import RenderKwargs, TargetType, Messageable
from .custom import CustomView


class ViewManager:
    def __init__(self) -> None:
        self.message: Optional[Message] = None
        self.discord_message: Optional[discord.Message] = None
        self.view: Optional[ui.View] = None
        self.started: bool = False
        self.update_lock: asyncio.Lock = asyncio.Lock()
        self.target_type: TargetType = TargetType.Normal
        self.view: CustomView = CustomView(self)

    def raise_for_started(self) -> None:
        if not self.started:
            raise Exception("View rendering is not started")

    async def send(self, target: Target, message: Message, **kwargs) -> None:
        if message.component is not None:
            message.component.make_view(self.view)

        if isinstance(target, Messageable):
            self.discord_message = await target.send(
                content=message.content,
                embed=message.embed,
                view=self.view
            )
        elif isinstance(target, discord.Interaction):
            await target.response.send_message(
                content=message.content,
                embed=message.embed or discord.utils.MISSING,
                view=self.view or discord.utils.MISSING
            )
            self.target_type = TargetType.Interaction
        elif isinstance(target, discord.Webhook):
            kwargs_ = {}
            for k, v in kwargs.items():
                kwargs_[k] = v if v is not None else discord.utils.MISSING
            self.discord_message = await target.send(
                content=message.content or discord.utils.MISSING,
                embed=message.embed or discord.utils.MISSING,
                view=self.view or discord.utils.MISSING,
                wait=True,
                **kwargs_
            )
            self.target_type = TargetType.Webhook

    async def start(
            self,
            target: Target,
            message: Message,
            **kwargs) -> None:
        if self.started:
            raise ValueError("This View has already started")

        await self.send(target, message, **kwargs)
        self.message = message
        self.started = True

    async def apply(self, apply_message: discord.Message, message: Message) -> None:
        if self.started:
            raise ValueError("This View has already started")

        if message.component is not None:
            message.component.make_view(self.view)

        self.discord_message = apply_message
        await self.discord_message.edit(
            content=message.content,
            embed=message.embed,
            view=self.view
        )
        self.message = message
        self.started = True

    async def update(self, message: Message) -> None:
        if self.target_type is TargetType.Interaction:
            return
        self.raise_for_started()
        async with self.update_lock:
            if self.message is None:
                return
            kwargs = await self.message.update(message, self.view)
            await self.render(**kwargs)

    async def render(self, **kwargs: RenderKwargs) -> None:
        if self.discord_message is None:
            return

        if self.target_type is TargetType.Webhook:
            kwargs_ = {}
            for k, v in kwargs.items():
                kwargs_[k] = v if v is not None else discord.utils.MISSING
        else:
            kwargs_ = kwargs

        await self.discord_message.edit(**kwargs_)
        if kwargs.get("view", None) is None:
            self.view = None
