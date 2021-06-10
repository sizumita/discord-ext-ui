from typing import List, Optional, Union, ClassVar

from discord import ui

from .item import Item

ViewItem = Union[Item, List[Item]]

Items = List[ViewItem]


class ViewBuilder:
    __discord_ui_view__: ClassVar[bool] = True

    def __init__(self, items: Optional[Items] = None) -> None:
        if items is None:
            items: Items = Items([])
        self.items = items

    def append(self, item: ViewItem) -> 'ViewBuilder':
        self.items.append(item)
        return self

    def insert(self, index: int, item: ViewItem) -> 'ViewBuilder':
        self.items.insert(index, item)
        return self

    def index(self, item: ViewItem) -> int:
        return self.items.index(item)

    def pop(self, index: int) -> Item:
        return self.items.pop(index)

    def remove(self, item: ViewItem) -> 'ViewBuilder':
        self.items.remove(item)
        return self

    def clear(self) -> 'ViewBuilder':
        self.items.clear()
        return self

    def build(self) -> ui.View:
        view = ui.View()

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
