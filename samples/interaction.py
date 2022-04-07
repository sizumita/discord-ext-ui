from discord.ext.ui import Button, View, ObservableObject, published, Message, ViewTracker, InteractionProvider
from discord.ext.ui.combine import PassThroughSubject

import discord
import os


bot = discord.Client(intents=discord.Intents.default())


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

    async def stop_(self, _):
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
                    .on_click(self.stop_)
                    .style(discord.ButtonStyle.danger)
            ]
        ])


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.is_command():
        view = SampleView()
        tracker = ViewTracker(view, timeout=None)
        await tracker.track(InteractionProvider(interaction))


bot.run(os.environ["DISCORD_BOT_TOKEN"])
