from __future__ import annotations


from typing import Any, Callable, TypeVar, Generic, Optional


class Publisher:
    def __init__(self):
        self.children: Optional[Publisher] = None
        self.parent: Optional[Publisher] = None
        self.subscribers: list[Callable[[Any], None]] = []

    def set_child(self, child: Publisher) -> Publisher:
        self.children = child
        return self

    def chain(self, new_publisher: Publisher) -> Publisher:
        new_publisher.parent = self
        self.set_child(new_publisher)
        return new_publisher

    def downstream(self, value: Any):
        """
        親に伝播する
        :param value:
        :return:
        """
        if self.parent is not None:
            self.parent.downstream(value)

    def upstream(self, value: Any):
        """
        子供に伝播する
        :param value:
        :return:
        """
        if self.children is not None:
            self.children.upstream(value)

        for func in self.subscribers:
            func(value)

    def dispatch(self) -> Any:
        """
        subscriberが追加された時に初回起動させる
        :return:
        """
        if self.parent is not None:
            self.parent.dispatch()

    def send(self, value: Any) -> None:
        self.downstream(value)

    def sink(self, func: Callable[[Any], None]) -> Publisher:
        self.subscribers.append(func)
        self.dispatch()
        return self

    def map(self, func: Callable[[Any], Any]) -> Publisher:
        new_publisher = MapPublisher(func)
        self.chain(new_publisher)
        return new_publisher


class MapPublisher(Publisher):
    def __init__(self, func: Callable[[Any], Any]) -> None:
        super().__init__()
        self.map_func = func

    def upstream(self, value: Any):
        if isinstance(value, list):
            value = [self.map_func(v) for v in value]
        else:
            value = self.map_func(value)

        for func in self.subscribers:
            func(value)
