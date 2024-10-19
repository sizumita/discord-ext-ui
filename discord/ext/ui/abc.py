from __future__ import annotations

import abc
import asyncio
import os
from abc import abstractmethod
from typing import TypeVar, Generic, TYPE_CHECKING, Callable, Optional, Awaitable, cast, Union
from typing_extensions import Self, TypeAlias

import discord


if TYPE_CHECKING:
    from .message import ViewMessage
    from .context import Context
    from .provider import ContextProvider
    from .signal import Signal

S = TypeVar("S", bound="Signal", covariant=True)
P = TypeVar("P", bound="ContextProvider", covariant=True)
ItemT = TypeVar("ItemT", bound=discord.ui.Item)
ViewElementHandler: TypeAlias = Callable[["Context", discord.Interaction, ItemT], Union[Awaitable[Optional[S]], Optional[S]]]


class Runnable(Generic[S, P], metaclass=abc.ABCMeta):
    @abstractmethod
    async def run(self, ctx: Context[P]) -> S:
        raise NotImplementedError()


class Displayable(Generic[S, P], metaclass=abc.ABCMeta):
    @abstractmethod
    async def appear(self, ctx: Context[P]) -> S:
        raise NotImplementedError()


class Observable(metaclass=abc.ABCMeta):
    @abstractmethod
    def update(self, name: str):
        raise NotImplementedError()


class Renderer(Generic[P], metaclass=abc.ABCMeta):
    @abstractmethod
    async def render(self, ctx: Context[P]) -> ViewMessage:
        raise NotImplementedError()


class ViewElement(Generic[S, P, ItemT], metaclass=abc.ABCMeta):
    def __init__(self, custom_id: Optional[str] = None) -> None:
        self.check_function: Optional[Callable[[Context, discord.Interaction], bool]] = None
        self.handler: Optional[ViewElementHandler] = None
        self._custom_id = custom_id or os.urandom(16).hex()
        self.is_custom_id_random = custom_id is None

    @abstractmethod
    def check(self, callback: Callable[[Context[P], discord.Interaction], bool]) -> Self:
        raise NotImplementedError()

    async def handle(self, context: Context[P], data: discord.Interaction, item: ItemT):
        if self.check_function is not None:
            check_result = self.check_function(context, data)
            if check_result is None or not check_result:
                return None
        if self.handler is not None:
            result = self.handler(context, data, item)
            if asyncio.iscoroutine(result):
                await context.scope.signal_queue.put(cast(Optional[S], await result))
                return
            await context.scope.signal_queue.put(cast(Optional[S], result))

    @staticmethod
    @abstractmethod
    def width() -> int:
        raise NotImplementedError()

    @property
    def custom_id(self) -> Optional[str]:
        return self._custom_id

    @property
    @abstractmethod
    def type(self) -> discord.ComponentType:
        raise NotImplementedError()

    @abstractmethod
    def to_ui_item(self, view: discord.ui.View, ctx: Context, row: int) -> discord.ui.Item:
        raise NotImplementedError()


class MessageId(metaclass=abc.ABCMeta):
    pass
