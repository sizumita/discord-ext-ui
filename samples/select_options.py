from typing import List

from discord.ext.ui import Component, View, Message, Select, SelectOption
from discord.ext import commands
import discord
import os

bot = commands.Bot("!")


class SampleView(View):
    def __init__(self, client):
        super().__init__(client)

    async def select_animal(self, interaction: discord.Interaction, selected: List[discord.SelectOption]) -> None:
        if "cat" in [i.label for i in selected]:
            await interaction.response.send_message("Oh! I like cat too!")
        else:
            await interaction.response.send_message("I see. I like cat.")

    async def body(self):
        return Message(
            content=f"select your favorite animals!",
            component=Component(items=[
                [
                    Select()
                    .options([
                        SelectOption("dog"),
                        SelectOption("cat"),
                        SelectOption("elephant"),
                        SelectOption("dug")
                    ]).on_select(self.select_animal)
                    .max_values(4)
                ]
            ])
        )


@bot.event
async def on_message(message):
    if message.content != "!test":
        return

    view = await SampleView(bot).setup()
    await message.channel.send(**view.build())


bot.run(os.environ["DISCORD_BOT_TOKEN"])
