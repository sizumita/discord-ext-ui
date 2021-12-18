from __future__ import annotations
from typing import Optional

from discord import ui


class Item:
    def to_discord_item(self, row: Optional[int]) -> ui.Item:
        pass
