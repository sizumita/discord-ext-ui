from __future__ import annotations
from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, TypeVar, Generic, Optional, cast

import discord

from .abc import MessageId

if TYPE_CHECKING:
    from .message import ViewMessage


Id = TypeVar("Id", bound=MessageId)


class ContextProvider(Generic[Id]):
    @abstractmethod
    async def send_new_message(self, message: ViewMessage, view: Optional[discord.ui.View]) -> Id:
        raise NotImplementedError()

    @abstractmethod
    async def send_lower_message(self, message: ViewMessage, view: Optional[discord.ui.View]) -> Id:
        raise NotImplementedError()

    @abstractmethod
    def stop_view(self, view: discord.ui.View) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_message(self, message_id: Id, message: ViewMessage, view: Optional[discord.ui.View]) -> None:
        raise NotImplementedError()


class DiscordMessageIdType(Enum):
    Message = 1
    Interaction = 2


class DiscordMessageId(MessageId):
    def __init__(self, typ: DiscordMessageIdType, *, message: Optional[discord.Message] = None, interaction: Optional[discord.Interaction] = None):
        self.type = typ
        self.message = message
        self.interaction = interaction


class DiscordProvider(ContextProvider[DiscordMessageId]):
    def __init__(self, client: discord.Client, channel: discord.abc.Messageable):
        self.channel = channel
        self.client = client

    async def send_new_message(self, message: ViewMessage, view: Optional[discord.ui.View]) -> DiscordMessageId:
        msg = await self.channel.send(
            content=message.content,
            embeds=message.embeds,
            view=view
        )
        return DiscordMessageId(DiscordMessageIdType.Message, message=msg)

    async def send_lower_message(self, message: ViewMessage, view: Optional[discord.ui.View]) -> Id:
        raise NotImplementedError()

    def stop_view(self, view: discord.ui.View) -> None:
        pass
        # view.stop()
        # self.client._connection._view_store.remove_view(view)

    async def update_message(self, message_id: DiscordMessageId, message: ViewMessage, view: Optional[discord.ui.View]) -> None:
        if message_id.type == DiscordMessageIdType.Message:
            print("editing")
            print(message_id.message)
            print(view)
            new_msg = await cast(discord.Message, message_id.message).edit(
                content=message.content,
                embeds=message.embeds or [],
                allowed_mentions=message.allowed_mentions,
                view=view,
            )
        elif message_id.type == DiscordMessageIdType.Interaction:
            raise NotImplementedError()
