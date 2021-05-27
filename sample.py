from discord.ext.ui import State, Component, Button, View, ObservedObject, Published
import discord
import os

client = discord.Client()


class SampleViewModel(ObservedObject):
    def __init__(self):
        super().__init__()
        self.num = Published(0)

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
        self.stop()

    async def body(self):
        return Component(
            f"test! {self.viewModel.num}",
            buttons=[
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
            ]
        )


@client.event
async def on_message(message):
    if message.content != "!test":
        return
    await SampleView().start(client, message.channel)


client.run(os.environ["DISCORD_BOT_TOKEN"])
