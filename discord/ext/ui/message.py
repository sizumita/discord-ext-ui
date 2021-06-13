from typing import Optional, Callable

import discord

from .component import Component
from .custom import CustomView
from .utils import _call_any


class Message:
    def __init__(self,
                 content: Optional[str] = None,
                 embed: Optional[discord.Embed] = None,
                 component: Optional[Component] = None) -> None:
        self.content: Optional[str] = content
        self.embed: Optional[discord.Embed] = embed
        self.component: Optional[Component] = component
        self.appear_func: Optional[Callable] = None
        self.disappear_func: Optional[Callable] = None

    async def update(self, other: 'Message', view: CustomView) -> dict:
        kwargs = {}
        if self.content != other.content:
            kwargs['content'] = other.content
            self.content = other.content

        if self.embed != other.embed:
            kwargs['embed'] = other.embed
            self.embed = other.embed

        if self.component != other.component:
            if other.component is None and self.component is not None:
                kwargs['view'] = None
                self.component = None
                view.replaced = True
            else:
                other.component.make_view(view)
                kwargs['view'] = view
                self.component = other.component

        return kwargs

    def on_appear(self, func: Callable) -> 'Message':
        self.appear_func = func
        return self

    def on_disappear(self, func: Callable) -> 'Message':
        self.disappear_func = func
        return self

    async def appear(self) -> None:
        if self.appear_func is not None:
            await _call_any(self.appear_func)

    async def disappear(self) -> None:
        if self.disappear_func is not None:
            await _call_any(self.disappear_func)
