from typing import Optional, List, Union, Callable, Any

from .combine import State, ObservedObject
from .message import Message

import discord
from discord import ui
from discord.ext import commands


class View:
    def __init__(self) -> None:
        self._watch_variables: List[str] = []
        self.bot: Optional[Union[discord.Client, commands.Bot]] = None
        self.message: Optional[Message] = None
        self.discord_message: Optional[discord.Message] = None
        self.view: Optional[ui.View] = None
        self.listeners: List[Callable] = []

    def add_listener(self, func: Callable, name: Optional[str] = None) -> None:
        if not isinstance(self.bot, commands.Bot):
            raise ValueError("bot must be commands.Bot")

        self.bot.add_listener(func, name)

    def remove_listener(self, func: Callable, name: Optional[str] = None) -> None:
        if not isinstance(self.bot, commands.Bot):
            raise ValueError("bot must be commands.Bot")

        self.bot.remove_listener(func, name)

    @staticmethod
    def listen(name: Optional[str] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            func.__listener__ = True  # type: ignore
            func.__listener_name__ = name or func.__name__  # type: ignore
            return func
        return decorator

    async def body(self) -> Message:
        return Message()

    async def start(self, bot: Union[discord.Client, commands.Bot], channel: discord.abc.Messageable) -> None:
        self.bot = bot
        self.message = await self.body()
        self.view, self.discord_message = await self.message.send(channel)
        await self.message.appear()
        for name in dir(self):
            member = getattr(self, name, None)
            if hasattr(member, "__listener__"):
                self.add_listener(member, getattr(member, "__listener_name__", None))
                self.listeners.append(member)

    async def stop(self) -> None:
        if self.message is None:
            return

        for listener in self.listeners:
            self.remove_listener(listener, getattr(listener, "__listener_name__", None))

        await self.message.disappear()
        if self.view is not None:
            self.view.stop()

    async def update(self) -> None:
        if self.message is None:
            return
        v = await self.message.update(self.discord_message, (await self.body()))
        if v is not None:
            self.view = v

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_watch_variables":
            object.__setattr__(self, key, value)
            return

        if isinstance(value, ObservedObject):
            value.view = self

        if not hasattr(self, key):
            if isinstance(value, State):
                self._watch_variables.append(key)
                object.__setattr__(self, key, value.value)
                return
        if isinstance(value, State):
            value = value.value

        if key in self._watch_variables:
            object.__setattr__(self, key, value)
            if self.bot is not None:
                self.bot.loop.create_task(self.update())
            return

        object.__setattr__(self, key, value)
