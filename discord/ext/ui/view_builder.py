from typing import List, Optional, Union

from discord import ui

from .item import Item

ViewItem = Union[Item, List[Item]]

Items = List[ViewItem]


class ViewBuilder:
    def __init__(self, items: Optional[Items] = None) -> None:
        self.items = items if items is not None else []

    def append(self, item: ViewItem) -> 'ViewBuilder':
        """Append Item to ViewBuilder.

        Parameters
        -----------
        item: Union[:class:`Item`, List[:class:`Item`]]
            Item or Item List to append.
        """
        self.items.append(item)
        return self

    def insert(self, index: int, item: ViewItem) -> 'ViewBuilder':
        self.items.insert(index, item)
        return self

    def index(self, item: ViewItem) -> int:
        return self.items.index(item)

    def pop(self, index: int) -> ViewItem:
        return self.items.pop(index)

    def remove(self, item: ViewItem) -> 'ViewBuilder':
        self.items.remove(item)
        return self

    def clear(self) -> 'ViewBuilder':
        self.items.clear()
        return self

    def build(self, *, timeout: Optional[int] = None) -> ui.View:
        view = ui.View(timeout=timeout)

        i = 0
        for item in self.items:
            if not isinstance(item, list):
                view.add_item(item.to_discord())
                continue
            for item_ in item:  # type: Item
                setattr(item_, "_row", i)
                view.add_item(item_.to_discord())
            i += 1

        return view
