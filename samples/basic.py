from discord.ext.ui import Button, View, ObservableObject, published, Message, ViewTracker, MessageProvider
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
    def __init__(self):
        super().__init__()
        self.viewModel = SampleViewModel()

    async def delete(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await self.stop()

    async def body(self):
        return Message()\
            .content(f"test! {self.viewModel.num}")\
            .items([
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


@bot.event
async def on_message(message: discord.Message):
    if message.content != "!test":
        return

    view = SampleView()
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


bot.run(os.environ["DISCORD_BOT_TOKEN"])
