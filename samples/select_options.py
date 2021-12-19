from typing import List

from discord.ext.ui import View, Message, Select, SelectOption, ViewTracker, MessageProvider
from discord.ext import commands
import discord
import os

bot = commands.Bot("!")


class SampleView(View):
    def __init__(self, client: discord.Client):
        super().__init__(client.loop)

    async def select_animal(self, interaction: discord.Interaction, selected: List[discord.SelectOption]) -> None:
        if "cat" in [i.label for i in selected]:
            await interaction.response.send_message("Oh! I like cat too!")
        else:
            await interaction.response.send_message("I see. I like cat.")

    async def body(self):
        return Message(
            f"select your favorite animals!",
            components=[
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
            ]
        )


@bot.event
async def on_message(message):
    if message.content != "!test":
        return

    view = SampleView(bot)
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


bot.run(os.environ["DISCORD_BOT_TOKEN"])
