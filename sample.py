from discord.ext.ui import State, Component, Button, View
import discord
import os

client = discord.Client()


class SampleView(View):
    def __init__(self):
        super().__init__()
        self.num = State(0)

    def countup(self):
        self.num += 1

    def countdown(self):
        self.num -= 1

    async def body(self):
        return Component(
            f"test! {self.num}",
            buttons=[
                Button("+1")
                .on_click(lambda x: self.countup())
                .style(discord.ButtonStyle.blurple),
                Button("-1")
                .on_click(lambda x: self.countdown())
                .style(discord.ButtonStyle.blurple)
            ]
        )


@client.event
async def on_message(message):
    if message.content != "!test":
        return
    await SampleView().start(client, message.channel)


client.run(os.environ["DISCORD_BOT_TOKEN"])
