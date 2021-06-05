import asyncio
from typing import Any, Callable

import discord


async def _call_any(func: Callable, *args: Any, **kwargs: Any) -> Any:
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


def async_interaction_partial(func: Callable, *args: Any, **kwargs: Any) -> Callable:
    async def callback(interaction: discord.Interaction) -> Any:
        return await func(interaction, *args, **kwargs)
    return callback


def interaction_partial(func: Callable, *args: Any, **kwargs: Any) -> Callable:
    def callback(interaction: discord.Interaction) -> Any:
        return func(interaction, *args, **kwargs)

    return callback
