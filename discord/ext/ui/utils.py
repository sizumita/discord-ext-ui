import asyncio
from typing import Any

import discord


async def _call_any(func, *args, **kwargs):
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


def async_interaction_partial(func, *args, **kwargs):
    async def callback(interaction: discord.Interaction) -> Any:
        return await func(interaction, *args, **kwargs)
    return callback


def interaction_partial(func, *args, **kwargs):
    def callback(interaction: discord.Interaction) -> Any:
        return func(interaction, *args, **kwargs)

    return callback
