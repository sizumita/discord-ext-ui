from typing import Any


class ValueAble:
    def __init__(self, default: Any = None):
        self.value = default

    def __getattr__(self, item):
        self.value.__getattr__(item)

    def __getattribute__(self, item):
        self.value.__getattribute__(item)
