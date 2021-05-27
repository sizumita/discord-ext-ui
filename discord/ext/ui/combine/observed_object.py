from typing import Any

from .published import Published


class ObservedObject:
    def __init__(self) -> None:
        self.view = None

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(getattr(self, key, None), Published):
            if not isinstance(value, Published):
                value = Published(value)
            super(ObservedObject, self).__setattr__(key, Published(value))
            if self.view is not None:
                self.view.bot.loop.create_task(self.view.update())
            return

        return super(ObservedObject, self).__setattr__(key, value)
