from typing import Optional, TYPE_CHECKING

from .message import Message
from .button import LinkButton

if TYPE_CHECKING:
    from .tracker import ViewTracker


class View:
    def __init__(self):
        self._tracker: Optional['ViewTracker'] = None

    async def body(self) -> Message:
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
        pass

    async def on_update(self) -> None:
        """
        Viewが更新された際に送信されます。
        """
        pass

    def stop(self):
        self._tracker.stop()
