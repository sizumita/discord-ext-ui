from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING, Any

from .message import Message
from .button import LinkButton
from .observable_object import ObservableObject

if TYPE_CHECKING:
    from .tracker import ViewTracker


class View:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self._tracker: Optional['ViewTracker'] = None
        self.loop = loop or asyncio.get_event_loop()

    async def body(self) -> Message | View:
        return Message()\
            .content("Hello World!\n\ncreated by discord-ext-ui from @sizumita")\
            .item(LinkButton("https://twitter.com/sizumita", "Twitter @sizumita"))\
            .item(LinkButton("https://github.com/sizumita/discord-ext-ui", "Github discord-ext-ui"))

    async def on_appear(self) -> None:
        """
        Viewが送信された際に実行されます。
        """
        pass

    async def on_disappear(self) -> None:
        """
        Viewがstopされた際に送信されます。
        """
        pass

    async def on_update(self) -> None:
        """
        Viewが更新された際に送信されます。
        """
        pass

    def stop(self):
        self._tracker.stop()
        self.loop.create_task(self.on_disappear())

    def update_sync(self):
        if self._tracker is not None:
            self.loop.create_task(self._tracker.update())

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, ObservableObject):
            value.view = self

        object.__setattr__(self, key, value)
