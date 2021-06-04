from typing import Any, List, Optional, TYPE_CHECKING

from .published import Published

if TYPE_CHECKING:
    from ..view import View


class ObservedObject:
    def __init__(self) -> None:
        self._watch_variables: List[str] = []
        self.view: Optional['View'] = None

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_watch_variables":
            object.__setattr__(self, key, value)
            return

        if not hasattr(self, key):
            if isinstance(value, Published) and hasattr(self, "_watch_variables"):
                self._watch_variables.append(key)
                object.__setattr__(self, key, value.value)
                return
        if isinstance(value, Published):
            value = value.value

        if key in getattr(self, "_watch_variables", []):
            object.__setattr__(self, key, value)
            if self.view is not None:
                self.view.update_sync()
            return

        return object.__setattr__(self, key, value)
