from typing import Optional, List, Union, Callable, Any

import discord
from discord import ui
from discord.ext import commands

from .combine import State, ObservedObject
from .message import Message
from .view_manager import ViewManager


class View:
    def __init__(self, client: Union[discord.Client, commands.Bot]) -> None:
        self._watch_variables: List[str] = []

        self.client: Union[discord.Client, commands.Bot] = client
        self.manager = ViewManager()
        self.discord_message: Optional[discord.Message] = None
        self.view: Optional[ui.View] = None

        self._listeners: List[Callable] = []

    def add_listener(self, func: Callable, name: Optional[str] = None) -> None:
        if not isinstance(self.client, commands.Bot):
            raise ValueError("bot must be commands.Bot")

        self.client.add_listener(func, name)

    def remove_listener(self, func: Callable, name: Optional[str] = None) -> None:
        if not isinstance(self.client, commands.Bot):
            raise ValueError("bot must be commands.Bot")

        self.client.remove_listener(func, name)

    @staticmethod
    def listen(name: Optional[str] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            setattr(func, "__listener__", True)
            setattr(func, "__listener_name__", name or func.__name__)
            return func
        return decorator

    async def body(self) -> Message:
        return Message()

    def get_message(self) -> discord.Message:
        """
        Returns message that this View is attended
        :return: discord.Message
        """
        return self.manager.discord_message

    async def start(self, channel: discord.abc.Messageable) -> None:
        await self.manager.start(channel, await self.body())
        await self.manager.message.appear()
        for name in dir(self):
            member = getattr(self, name, None)
            if hasattr(member, "__listener__"):
                self.add_listener(member, getattr(member, "__listener_name__", None))
                self._listeners.append(member)

    async def stop(self) -> None:
        self.manager.raise_for_started()

        for listener in self._listeners:
            self.remove_listener(listener, getattr(listener, "__listener_name__", None))

        await self.manager.message.disappear()
        if self.view is not None:
            self.view.stop()

    async def update(self) -> None:
        self.manager.raise_for_started()
        await self.manager.update((await self.body()))

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
            if self.client is not None:
                self.client.loop.create_task(self.update())
            return

        object.__setattr__(self, key, value)
