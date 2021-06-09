from typing import Any, TypeVar

from .observable_object import ObservableObject

T = TypeVar('T')


def published(name: str):
    def getter(instance: T) -> Any:
        return instance.__dict__[name]

    def setter(instance: T, value: Any) -> None:
        instance.__dict__[name] = value
        if isinstance(instance, ObservableObject):
            instance.notify()

    return property(getter, setter)
