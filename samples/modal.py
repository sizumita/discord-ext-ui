from discord.ext.ui import Button, View, Message, ViewTracker, MessageProvider, Modal
import discord
from discord.ui import TextInput
import os


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


class SampleView(View):
    def __init__(self):
        super().__init__()

    async def delete(self, interaction: discord.Interaction):
        await interaction.message.delete()
        self.stop()

    async def body(self):
        return Message(
            components=[
                Button("show modal")
                .modal(Modal("test", [
                    TextInput(label="test dayo", default="hello!")
                ]))
            ]
        )


@client.event
async def on_message(message: discord.Message):
    if message.content != "!test":
        return

    view = SampleView()
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


client.run(os.environ["DISCORD_BOT_TOKEN"])
