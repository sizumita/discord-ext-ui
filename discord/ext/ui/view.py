from typing import Optional

from .combine import State, ObservedObject
from .component import Component

from discord import ui


class View:
    def __init__(self):
        self._watch_variables = []
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
        if key == "_watch_variables":
            object.__setattr__(self, key, value)
            return

        if isinstance(value, ObservedObject):
            value.view = self

        if not hasattr(self, key):
            if isinstance(value, State):
                self._watch_variables.append(key)
                object.__setattr__(self, key, value.value)
                return
        if isinstance(value, State):
            value = value.value

        if key in self._watch_variables:
            object.__setattr__(self, key, value)
            self.bot.loop.create_task(self.update())
            return

        object.__setattr__(self, key, value)
