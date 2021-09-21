from typing import Optional, List, Union

from discord import ui

from .item import Item


class Component:
    def __init__(self, items: Optional[List[Union[Item, List[Item]]]] = None) -> None:
        self.items: List[Union[Item, List[Item]]] = [] if items is None else items

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Component):
            return False

        return self.items == other.items

    def make(self, view: ui.View) -> None:
        view.clear_items()
        i = 0
        for item in self.items:
            if not isinstance(item, list):
                if item._hide:
                    continue
                view.add_item(item.to_discord())
                continue
            for item_ in item:  # type: Item
                setattr(item_, "_row", i)
                if item_._hide:
                    continue
                view.add_item(item_.to_discord())
            i += 1
