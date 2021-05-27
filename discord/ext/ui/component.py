from typing import Optional, List, Union, Tuple

from discord import ui
from discord.abc import Messageable
from discord import Embed
import discord

from .button import Button


class Component:
    def __init__(self,
                 content: Optional[str] = None,
                 embed: Optional[Embed] = None,
                 buttons: Optional[List[Union[Button, List[Button]]]] = None) -> None:
        self.content = content
        self.embed = embed
        self.buttons = buttons

    def make_view(self) -> ui.View:
        view = ui.View()
        i = 1
        for button in self.buttons:
            if not isinstance(button, list):
                view.add_item(button.to_discord_button())
                continue
            for button_ in button:  # type: Button
                button_._group = i
                view.add_item(button_.to_discord_button())
            i += 1
        return view

    async def send(self, channel: Messageable) -> Tuple[ui.View, discord.Message]:
        view = self.make_view()
        return view, await channel.send(content=self.content, embed=self.embed, view=view)

    async def update(self, message: discord.Message) -> ui.View:
        view = self.make_view()
        await message.edit(content=self.content, embed=self.embed, view=view)
        return view
