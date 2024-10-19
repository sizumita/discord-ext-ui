from __future__ import annotations
from typing import Optional, Generic, TypeVar, TYPE_CHECKING, Any
import discord

from .provider import ContextProvider
from .signal import Signal
from .fake import FakeView

if TYPE_CHECKING:
    from .abc import ViewElement
    from .context import Context


S = TypeVar("S", bound=Signal, covariant=True)
P = TypeVar("P", bound=ContextProvider, covariant=True)


class ViewMessage(Generic[S, P]):
    def __init__(
            self,
            *,
            content: Optional[str] = None,
            embeds: Optional[list[discord.Embed]] = None,
            allowed_mentions: Optional[discord.AllowedMentions] = None,
            elements: Optional[list[list[ViewElement[S, P, Any]]]] = None
    ) -> None:
        self.content = content
        self.embeds = embeds
        self.allowed_mentions = allowed_mentions
        self.elements = elements

    def get_discord_ui_view(self, context: Context[P]) -> Optional[discord.ui.View]:
        """
        elementsがある場合はViewを返す
        """
        if len(self.elements or []) == 0:
            return None
        view = FakeView()
        items: list[discord.ui.Item] = []
        for (nth, row) in enumerate(self.elements or []):
            for element in row:
                items.append(element.to_ui_item(view, context, nth+1))
        view.set_items(items)

        return view
