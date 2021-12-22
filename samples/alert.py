import asyncio
import os

import discord

from discord.ext.ui import Button, Message, ViewTracker, MessageProvider, Alert, ActionButton, View, state


client = discord.Client()


class SampleView(View):
    content = state("content")

    def __init__(self):
        super().__init__()
        self.content = "編集中..."

    async def show_alert(self, interaction: discord.Interaction):
        alert = Alert("編集を終了しますか？", "", [
            ActionButton("いいえ", discord.ButtonStyle.blurple, False),
            ActionButton("はい", discord.ButtonStyle.danger, True)
        ], ephemeral=True)
        result = await alert.wait_for_click(interaction)
        if result:
            self.content = "編集を終了しました。"

    async def body(self):
        return Message()\
            .content(self.content)\
            .items([
                Button("終わる")
                .on_click(self.show_alert)
                .style(discord.ButtonStyle.danger)
                .disabled(self.content != "編集中..."),
        ])


@client.event
async def on_message(message: discord.Message):
    if message.content != "!test":
        return

    view = SampleView()
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


client.run(os.environ["DISCORD_BOT_TOKEN"])
