from discord.ext.ui import Component, Button, View, ObservableObject, published, Message
from discord.ext import commands
import discord
import os

bot = commands.Bot("!")


class SampleViewModel(ObservableObject):
    num = published('num')

    def __init__(self):
        super().__init__()
        self.num = 0

    def countup(self):
        self.num += 1

    def countdown(self):
        self.num -= 1


class SampleView(View):
    def __init__(self, client):
        super().__init__(client)
        self.viewModel = SampleViewModel()

    async def delete(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await self.stop()

    async def add_reaction(self):
        await self.message.add_reaction("\U0001f44d")

    @View.listen(name="on_reaction_add")
    async def watch_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if reaction.message == self.discord_message \
                and str(reaction.emoji) == "\U0001f44d":
            self.viewModel.countup()

    async def body(self):
        return Message(
            content=f"test! {self.viewModel.num}",
            component=Component(items=[
                [
                    Button("+1")
                    .on_click(lambda x: self.viewModel.countup())
                    .style(discord.ButtonStyle.blurple),

                    Button("-1")
                    .on_click(lambda x: self.viewModel.countdown())
                    .style(discord.ButtonStyle.blurple)
                ],
                [
                    Button("終わる")
                    .on_click(self.delete)
                    .style(discord.ButtonStyle.danger)
                ]
            ])
        ).on_appear(self.add_reaction)


@bot.event
async def on_message(message):
    if message.content != "!test":
        return

    await SampleView(bot).start(message.channel)


bot.run(os.environ["DISCORD_BOT_TOKEN"])
