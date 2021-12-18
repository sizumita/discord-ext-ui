from __future__ import annotations
from typing import Any

from .publisher import Publisher


class Just(Publisher):
    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value: Any = value

    def dispatch(self) -> Any:
        self.upstream(self.value)

    def send(self, value: Any) -> None:
        raise NotImplementedError
