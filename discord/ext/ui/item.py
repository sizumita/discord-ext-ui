from typing import Any, Callable

import discord


class Item:
    def to_discord(self) -> Any:
        pass

    def check(self, func: Callable[[discord.Interaction], bool]) -> 'Item':
        pass
