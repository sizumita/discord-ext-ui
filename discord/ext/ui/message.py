from __future__ import annotations
from typing import Union

import discord
from discord import ui

from .item import Item


class Message:
    def __init__(
            self,
            content: str = "",
            embeds: list[discord.Embed] = None,
            components: list[Union[list[Item], Item]] = None):
        self._content = content
        self._embeds: list[discord.Embed] = embeds or []
        self._components: list[Union[list[Item], Item]] = components or []

    def content(self, content: str) -> Message:
        self._content = content
        return self

    def embed(self, embed: discord.Embed) -> Message:
        self._embeds.append(embed)
        return self

    def embeds(self, embeds: list[discord.Embed]) -> Message:
        self._embeds.extend(embeds)
        return self

    def item(self, item: Union[list[Item], Item]) -> Message:
        self._components.append(item)
        return self

    def items(self, items: list[Union[list[Item], Item]]) -> Message:
        self._components.extend(items)
        return self

    def get_discord_items(self) -> list[ui.Item]:
        row = 0
        items = []
        for component in self._components:
            if isinstance(component, list):
                for sub_component in component:  # type: Item
                    items.append(sub_component.to_discord_item(row))
                row += 1
            else:
                items.append(component.to_discord_item(None))

        return items

    def __eq__(self, other: Message) -> bool:
        return self._components == other._components\
               and self._embeds == other._embeds\
               and self._content == other._content
