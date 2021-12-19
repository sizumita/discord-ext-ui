from __future__ import annotations
from typing import Any

from .publisher import Publisher


class Subject(Publisher):
    def send(self, value: Any) -> None:
        self.downstream(value)


class PassThroughSubject(Subject):
    def downstream(self, value: Any):
        self.upstream(value)
