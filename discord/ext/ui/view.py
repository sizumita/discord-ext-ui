from typing import Optional

from .combine import State, ObservedObject
from .component import Component

from discord import ui


class View:
    def __init__(self):
        self.bot = None
        self.message = None
        self.view: Optional[ui.View] = None

    async def body(self):
        return Component()

    async def start(self, bot, channel):
        self.bot = bot
        self.view, self.message = await (await self.body()).send(channel)

    def stop(self):
        if self.view is not None:
            self.view.stop()

    async def update(self):
        self.view = await (await self.body()).update(self.message)

    def __setattr__(self, key, value):
        if isinstance(getattr(self, key, None), State):
            if not isinstance(value, State):
                value = State(value)
            super(View, self).__setattr__(key, value)
            self.bot.loop.create_task(self.update())
            return
        if isinstance(value, ObservedObject):
            value.view = self

        super(View, self).__setattr__(key, value)
