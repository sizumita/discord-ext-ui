from typing import Optional

import discord
from discord import ui

from .item import Item


class LinkButton(Item):
    def __init__(self, url: str, label: str):
        self.url = url
        self.label = label

    def to_discord_item(self, row: Optional[int]) -> ui.Item:
        return ui.Button(style=discord.ButtonStyle.link, label=self.label, url=self.url)
