from __future__ import annotations

import asyncio
from typing import TypeVar, TYPE_CHECKING, Generic, Optional

import discord.ui

from .signal import Signal
from .checkpoint import Checkpoint
from .provider import ContextProvider

if TYPE_CHECKING:
    from .abc import Displayable, MessageId
    from .message import ViewMessage

P = TypeVar("P", bound=ContextProvider, covariant=True)
S = TypeVar("S", bound=Signal, covariant=True)


class Context(Generic[P]):
    def __init__(self, provider: P) -> None:
        self.provider: P = provider
        self.scope = Scope()

    def checkpoint(self, displayable: "Displayable[S, P]") -> Checkpoint[S, P]:
        return Checkpoint(self, displayable)

    async def render(self, message: ViewMessage):
        print(self.scope.present is None)
        print(self.scope.message_equals(message))
        if self.scope.present is None:
            if self.scope.view is not None:
                self.provider.stop_view(self.scope.view)
                del self.scope.view
                self.scope.view = None

            view = message.get_discord_ui_view(self)
            msg_id = await self.provider.send_new_message(message, view)
            self.scope.update(message)
            self.scope.set_message_id(msg_id)
            self.scope.view = view
        else:
            if not self.scope.message_equals(message):
                if self.scope.view is not None:
                    self.provider.stop_view(self.scope.view)
                    del self.scope.view
                    self.scope.view = None

                view = message.get_discord_ui_view(self)
                await self.provider.update_message(self.scope.message_id, message, view)
                self.scope.view = view
                self.scope.update(message)


class Scope:
    def __init__(self, *, parent: Optional[Scope] = None, before: Optional[Scope] = None):
        self.parent = parent
        self.before = before
        self.signal_queue: asyncio.Queue = asyncio.Queue(maxsize=1)
        self.present: Optional[ViewMessage] = None
        self.message_id: Optional[MessageId] = None
        self.view: Optional[discord.ui.View] = None

    def create_child(self) -> Scope:
        return Scope(parent=self)

    def create_next(self) -> Scope:
        return Scope(before=self)

    def set_message_id(self, msg_id: MessageId):
        self.message_id = msg_id

    def update(self, message: ViewMessage) -> None:
        self.present = message

    def message_equals(self, other: ViewMessage) -> bool:
        if self.present is None:
            return False
        return self.present.content == other.content and self.present.embeds == other.embeds and self.present.elements == other.elements and self.present.allowed_mentions == other.allowed_mentions
