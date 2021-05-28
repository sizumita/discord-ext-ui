from typing import Any


class ValueAble:
    def __init__(self, default: Any = None):
        setattr(self, "value", default)

    def __getattribute__(self, item):
        if item == "value":
            return object.__getattribute__(self, item)
        self.value.__getattribute__(item)
