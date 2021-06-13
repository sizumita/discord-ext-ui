from typing import Optional, TypedDict
from enum import Enum, auto

import discord
from discord import ui
from discord.ext import commands


class RenderKwargs(TypedDict, total=False):
    content: Optional[str]
    embed: Optional[discord.Embed]
    view: Optional[ui.View]


class TargetType(Enum):
    Normal = auto()
    Interaction = auto()
    Webhook = auto()


Messageable = (
    discord.TextChannel,
    discord.GroupChannel,
    commands.Context,
    discord.DMChannel,
    discord.User,
    discord.Member
)
