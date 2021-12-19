from __future__ import annotations


from typing import Any, Callable, Optional


class Publisher:
    def __init__(self):
        self.child: Optional[Publisher] = None
        self.parent: Optional[Publisher] = None
        self.subscribers: list[Callable[[Any], None]] = []

    def set_child(self, child: Publisher) -> Publisher:
        self.child = child
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
        if self.child is not None:
            self.child.upstream(value)

        for func in self.subscribers:
            func(value)

    def dispatch(self) -> Any:
        """
        subscriberが追加された時に初回起動させる
        :return:
        """
        if self.parent is not None:
            self.parent.dispatch()

    def sink(self, func: Callable[[Any], None]) -> Publisher:
        if self.child is not None:
            self.child.sink(func)
            return self
        self.subscribers.append(func)
        self.dispatch()
        return self

    def map(self, func: Callable[[Any], Any]) -> Publisher:
        if self.child is not None:
            self.child.map(func)
            return self
        new_publisher = MapPublisher(func)
        self.chain(new_publisher)
        return self


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
