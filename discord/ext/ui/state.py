from typing import TypeVar, Generic, Type

from .abc import Observable
from .error import UnreachableError

T = TypeVar("T")
C = TypeVar("C")


class State(Generic[T], object):
    def __init__(self, default: T):
        self.default = default
        self.name: str = ""
        self.private_name: str = ""

    def __set_name__(self, owner: C, name: str):
        self.name = name
        self.private_name = f"_{name}"

    def __set__(self, instance: C, value: T) -> None:
        if isinstance(instance, Observable):
            instance.update(self.name)
        setattr(instance, self.private_name, value)

    def __get__(self, instance: C, owner: Type[C]) -> T:
        value = getattr(instance, self.private_name, self.default)
        return value

    @property
    def obj(self) -> T:
        raise UnreachableError()

    def __getattribute__(self, item: str):
        if item == "obj":
            return self
        return object.__getattribute__(self, item)


def state(default: T) -> T:
    return State(default).obj
