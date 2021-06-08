from __future__ import annotations

from typing import Optional, TypedDict

import discord
from discord import ui


class RenderKwargs(TypedDict, total=False):
    content: Optional[str]
    embed: Optional[discord.Embed]
    view: Optional[ui.View]
