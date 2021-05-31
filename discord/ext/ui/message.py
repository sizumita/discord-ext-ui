from typing import Optional, Tuple, Callable

import discord
from discord import ui

from .component import Component
from .utils import _call_any


class Message:
    def __init__(self,
                 content: Optional[str] = None,
                 embed: Optional[discord.Embed] = None,
                 file: Optional[discord.File] = None,
                 component: Optional[Component] = None) -> None:
        self.content: Optional[str] = content
        self.file: Optional[discord.File] = file
        self.embed: Optional[discord.Embed] = embed
        self.component: Optional[Component] = component
        self.appear_func: Optional[Callable] = None
        self.disappear_func: Optional[Callable] = None

    async def send(self, channel: discord.abc.Messageable) -> Tuple[ui.View, discord.Message]:
        if self.component is None:
            raise ValueError("component is None")

        view = self.component.make_view()
        return view, await channel.send(content=self.content, embed=self.embed, view=view)

    async def update(self, other: 'Message') -> dict:
        kwargs = {}
        if self.content != other.content:
            kwargs['content'] = other.content
            self.content = other.content

        if other.embed is None:
            kwargs['embed'] = None
            self.embed = None
        elif self.embed != other.embed:
            kwargs['embed'] = other.embed
            self.embed = other.embed

        if other.component is None:
            kwargs['view'] = None
            self.component = None
        elif self.component != other.component:
            kwargs['view'] = other.component.make_view() if other.component is not None else None
            self.component = other.component

        if other.file is None:
            kwargs['file'] = None
            self.file = None
        elif self.file is None and other.file is not None:
            kwargs['file'] = other.file
            self.file = other.file
        elif self.file is not None and self.file.fp.read() != other.file.fp.read():
            other.file.reset()
            self.file.reset()
            kwargs['file'] = other.file
            self.file = other.file

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
