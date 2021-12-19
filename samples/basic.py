from discord.ext.ui import Button, View, ObservableObject, published, Message, ViewTracker, MessageProvider
from discord.ext.ui.combine import PassThroughSubject
import discord
import os


client = discord.Client()


class SampleViewModel(ObservableObject):
    num = published('num')

    def __init__(self):
        super().__init__()
        self.num = 0
        self.sub = PassThroughSubject().sink(self.change_count)

    def change_count(self, diff: int):
        self.num += diff


class SampleView(View):
    def __init__(self):
        super().__init__()
        self.viewModel = SampleViewModel()

    async def delete(self, interaction: discord.Interaction):
        await interaction.message.delete()
        self.stop()

    async def body(self):
        return Message()\
            .content(f"test! {self.viewModel.num}")\
            .items([
            [
                Button("+1")
                    .on_click(lambda _: self.viewModel.sub.send(1))
                    .style(discord.ButtonStyle.blurple),

                Button("-1")
                    .on_click(lambda _: self.viewModel.sub.send(-1))
                    .style(discord.ButtonStyle.blurple)
            ],
            [
                Button("終わる")
                    .on_click(self.delete)
                    .style(discord.ButtonStyle.danger)
            ]
        ])


@client.event
async def on_message(message: discord.Message):
    if message.content != "!test":
        return

    view = SampleView()
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


client.run(os.environ["DISCORD_BOT_TOKEN"])
