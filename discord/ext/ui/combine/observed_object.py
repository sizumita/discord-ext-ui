from typing import Any

from .published import Published


class ObservedObject:
    def __init__(self) -> None:
        self._watch_variables = []
        self.view = None

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_watch_variables":
            object.__setattr__(self, key, value)
            return

        if not hasattr(self, key):
            if isinstance(value, Published):
                self._watch_variables.append(key)
                object.__setattr__(self, key, value.value)
                return
        if isinstance(value, Published):
            value = value.value

        if key in self._watch_variables:
            object.__setattr__(self, key, value)
            self.view.bot.loop.create_task(self.view.update())
            return

        return object.__setattr__(self, key, value)
