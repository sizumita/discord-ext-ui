from typing import Optional, List, Union, Callable, Any

import discord
from discord import ui
from discord.ext import commands

from .combine import ObservableObject
from .message import Message
from .view_manager import ViewManager
from .types.view import Target


class View:
    def __init__(self, state: Union[discord.Client, commands.Bot]) -> None:
        self._state: Union[discord.Client, commands.Bot] = state
        self.manager: ViewManager = ViewManager()
        self.discord_message: Optional[discord.Message] = None
        self.view: Optional[ui.View] = None

        self._listeners: List[Callable] = []

    @property
    def message(self) -> Optional[discord.Message]:
        """Optional[:class:`discord.Message`]: The message that this View is attached."""
        return self.manager.discord_message

    def add_listener(self, func: Callable, name: Optional[str] = None) -> None:
        """Add Listener to ext.commands.Bot.

        Parameters
        -----------
        func: :ref:`coroutine <coroutine>`
            The function to call.
        name: Optional[:class:`str`]
            The name of the event to listen for. Defaults to ``func.__name__``.
        """
        if not isinstance(self._state, commands.Bot):
            raise ValueError("bot must be commands.Bot")

        self._state.add_listener(func, name)

    def remove_listener(self, func: Callable, name: Optional[str] = None) -> None:
        """Remove Listener from ext.commands.Bot.

        Parameters
        -----------
        func: :ref:`coroutine <coroutine>`
            The function to remove.
        name: Optional[:class:`str`]
            The name of the event to listen for. Defaults to ``func.__name__``.
        """
        if not isinstance(self._state, commands.Bot):
            raise ValueError("bot must be commands.Bot")

        self._state.remove_listener(func, name)

    @staticmethod
    def listen(name: Optional[str] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            setattr(func, "__listener__", True)
            setattr(func, "__listener_name__", name or func.__name__)
            return func
        return decorator

    async def body(self) -> Message:
        return Message()

    def _apply_listener(self) -> None:
        for name in dir(self):
            member = getattr(self, name, None)
            if hasattr(member, "__listener__"):
                self.add_listener(member, getattr(member, "__listener_name__", None))
                self._listeners.append(member)

    async def start(self, target: Target, **kwargs) -> None:
        """Send a Message to channel and attach View to it.

        Parameters
        -----------
        target: Union[:class:`discord.abc.Messageable`, :class:`discord.Interaction`, :class:`discord.Webhook`]
            The target to send.
        """
        await self.manager.start(target, await self.body(), **kwargs)
        if self.manager.message is not None:
            await self.manager.message.appear()
            self._apply_listener()

    async def apply(self, apply_message: discord.Message) -> None:
        """Attach View to apply_message.

        Parameters
        -----------
        apply_message: :class:`discord.Message`
            The Message to attach.
        """
        await self.manager.apply(apply_message, await self.body())
        if self.manager.message is not None:
            await self.manager.message.appear()
            self._apply_listener()

    async def stop(self) -> None:
        """Stop View listener and Interaction."""
        self.manager.raise_for_started()

        for listener in self._listeners:
            self.remove_listener(listener, getattr(listener, "__listener_name__", None))

        if self.manager.message is not None:
            await self.manager.message.disappear()

        if self.view is not None:
            self.view.stop()

    async def update(self) -> None:
        self.manager.raise_for_started()
        await self.manager.update((await self.body()))

    def update_sync(self) -> None:
        if self._state is not None:
            self._state.loop.create_task(self.update())

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, ObservableObject):
            value.view = self

        object.__setattr__(self, key, value)
