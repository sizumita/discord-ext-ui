import asyncio
from typing import Optional, List, Union, Callable, Any, Dict

import discord
from discord import ui
from discord.ext import commands

from .combine import ObservableObject
from .message import Message
from .types.view import Target, BuildResponse, Messageable, TargetType


class View(ui.View):
    def __init__(self, state: Union[discord.Client, commands.Bot]) -> None:
        super(View, self).__init__(timeout=None)
        self._state: Union[discord.Client, commands.Bot] = state

        self._listeners: List[Callable] = []
        self._view_message: Optional[Message] = None
        self._discord_message: Optional[discord.Message] = None
        self.started: asyncio.Event = asyncio.Event()
        self._target_type: TargetType = TargetType.Normal

    def __init_subclass__(cls) -> None:
        pass

    def refresh(self, components: List[discord.Component]) -> None:
        pass

    def build(self) -> BuildResponse:
        return dict(
            content=self._view_message.content,
            embed=self._view_message.embed,
            view=self
        )

    @property
    def message(self) -> Optional[discord.Message]:
        """Optional[:class:`discord.Message`]: The message that this View is attached."""
        return self._discord_message

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

    async def stop(self) -> None:
        """Stop View listener and Interaction."""
        self._raise_for_not_started()

        for listener in self._listeners:
            self.remove_listener(listener, getattr(listener, "__listener_name__", None))

        await self._view_message.disappear()

        super(View, self).stop()

    async def update(self) -> None:
        if not self.started.is_set():
            return
        if self._discord_message is None:
            return
        message: Message = await self.body()
        kwargs = await self._view_message.update(message, self)
        await self._discord_message.edit(**kwargs)

    async def setup(self) -> 'View':
        self._view_message = await self.body()
        if self._view_message.component is not None:
            self._view_message.component.make(self)

        return self

    def _start_listening_from_store(self, store: discord.ui.view.ViewStore) -> None:
        if not self.started.is_set():
            self._apply_listener()
            if self._view_message is not None:
                self._state.loop.create_task(self._view_message.appear())
            self.started.set()
        super(View, self)._start_listening_from_store(store)

    def update_sync(self) -> None:
        if self._state is not None:
            self._state.loop.create_task(self.update())

    def _set_message(self, message: discord.Message) -> None:
        self._discord_message = message

    async def _scheduled_task(self, item: ui.Item, interaction: discord.Interaction) -> None:
        if self._discord_message is None:
            self._set_message(interaction.message)
        await super(View, self)._scheduled_task(item, interaction)

    def _raise_for_not_started(self) -> None:
        if not self.started.is_set():
            raise Exception("View rendering is not starting")

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, ObservableObject):
            value.view = self

        object.__setattr__(self, key, value)

    async def start(self, target: Target, **kwargs) -> None:
        """Send a Message to channel and attach View to it.

        Parameters
        -----------
        target: Union[:class:`discord.abc.Messageable`, :class:`discord.Interaction`, :class:`discord.Webhook`]
            The target to send.
        """
        await self.setup()
        if isinstance(target, Messageable):
            self._discord_message = await target.send(**self.build())
        elif isinstance(target, discord.Interaction):
            await target.response.send_message(
                content=self._view_message.content,
                embed=self._view_message.embed or discord.utils.MISSING,
                view=self
            )
            self._target_type = TargetType.Interaction
        elif isinstance(target, discord.Webhook):
            kwargs_ = {}
            for k, v in kwargs.items():
                kwargs_[k] = v if v is not None else discord.utils.MISSING
            self._discord_message = await target.send(
                content=self._view_message.content or discord.utils.MISSING,
                embed=self._view_message.embed or discord.utils.MISSING,
                view=self,
                wait=True,
                **kwargs_
            )
            self._target_type = TargetType.Webhook

    async def apply(self, apply_message: discord.Message) -> None:
        """Attach View to apply_message.

        Parameters
        -----------
        apply_message: :class:`discord.Message`
            The Message to attach.
        """
        await self.setup()
        self._discord_message = apply_message
        await self._discord_message.edit(**self.build())
