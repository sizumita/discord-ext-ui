from __future__ import annotations

import asyncio
from typing import Any

import discord

from .view import View
from .button import Button
from .message import Message
from .tracker import ViewTracker
from .provider import InteractionProvider


class Alert(View):
    def __init__(self, title: str, text: str, buttons: list[ActionButton | list[ActionButton]], ephemeral: bool = False):
        super().__init__()
        self.title = title
        self.text = text
        self.buttons = buttons
        self.ephemeral = ephemeral
        self.clicked = asyncio.Future()

    def _set_func(self):
        buttons = []
        for button in self.buttons:
            if isinstance(button, list):
                buttons_ = []
                for button_ in button:  # type: ActionButton
                    buttons_.append(button_.set_future(self.clicked))
                buttons.append(buttons_)
            else:
                buttons.append(button.set_future(self.clicked))

        self.buttons = buttons

    async def body(self) -> Message | View:
        self._set_func()
        return Message(embeds=[
            discord.Embed(title=self.title, description=self.text, colour=discord.Colour.blurple())
        ], components=self.buttons)

    async def wait_for_click(self, interaction: discord.Interaction, timeout: float | None = 180.0):
        tracker = ViewTracker(self, timeout)
        await tracker.track(InteractionProvider(interaction, ephemeral=self.ephemeral))
        await self.clicked
        self.stop()
        return self.clicked.result()


class ActionButton(Button):
    def __init__(self, label: str, style: discord.ButtonStyle, value: Any, **kwargs):
        super().__init__(label=label, style=style, **kwargs)
        self.value = value
        self.clicked: asyncio.Future | None = None

    def set_future(self, future: asyncio.Future) -> Button:
        self.clicked = future
        super(ActionButton, self).on_click(self.selected)
        return self

    def selected(self, _: discord.Interaction):
        self.clicked.set_result(self.value)
