from __future__ import annotations
from typing import Union

import discord
from discord import ui

from .item import Item


class Message:
    def __init__(self):
        self.content_ = None
        self.embeds_: list[discord.Embed] = []
        self.components_: list[Union[list[Item], Item]] = []

    def content(self, content: str) -> Message:
        self.content_ = content
        return self

    def embed(self, embed: discord.Embed) -> Message:
        self.embeds_.append(embed)
        return self

    def embeds(self, embeds: list[discord.Embed]) -> Message:
        self.embeds_.extend(embeds)
        return self

    def item(self, item: Union[list[Item], Item]) -> Message:
        self.components_.append(item)
        return self

    def items(self, items: list[Union[list[Item], Item]]) -> Message:
        self.components_.extend(items)
        return self

    def get_discord_items(self) -> list[ui.Item]:
        row = 0
        items = []
        for component in self.components_:
            if isinstance(component, list):
                for sub_component in component:  # type: Item
                    items.append(sub_component.to_discord_item(row))
                row += 1
            else:
                items.append(component.to_discord_item(None))

        return items
