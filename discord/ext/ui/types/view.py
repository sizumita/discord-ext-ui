from typing import Union, TypedDict, Optional
from enum import Enum, auto

import discord
from discord import ui
from discord.ext import commands

Target = Union[discord.abc.Messageable, discord.Interaction, discord.Webhook]


Messageable = (
    discord.TextChannel,
    discord.GroupChannel,
    commands.Context,
    discord.DMChannel,
    discord.User,
    discord.Member
)


class BuildResponse(TypedDict, total=False):
    content: Optional[str]
    embed: Optional[discord.Embed]
    view: Optional[discord.ui.View]


class RenderKwargs(TypedDict, total=False):
    content: Optional[str]
    embed: Optional[discord.Embed]
    view: Optional[ui.View]


class TargetType(Enum):
    Normal = auto()
    Interaction = auto()
    Webhook = auto()
