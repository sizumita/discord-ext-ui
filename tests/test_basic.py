import uuid

import discord
import pytest

from ext.ui import Runner, ContextProvider, RunnerPool, Flow, Signal, DiscordProvider, Context, View, state, Button
from ext.ui.message import ViewMessage


class MyView(View[Signal, DiscordProvider]):
    async def callback(self, c: Context[Signal], interaction: discord.Interaction, item: discord.ui.Button) -> Signal | None:
        print(item)
        await interaction.response.send_message("ok")
        return None

    async def render(self, ctx: Context[DiscordProvider]) -> ViewMessage[Signal, DiscordProvider]:
        return ViewMessage(
            content="abc",
            elements=[
                [
                    Button(label="test")
                    .on_click(self.callback)
                ]
            ]
        )


class MyFlow(Flow[Signal, DiscordProvider]):
    async def run(self, ctx: Context[DiscordProvider]) -> Signal:
        await ctx.checkpoint(MyView()).display()
        return Signal("name")


client = discord.Client(intents=discord.Intents.all())
pool = RunnerPool()


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content == "abc":
        provider = DiscordProvider(message.channel)
        runner = Runner(provider)
        pool.register(runner)
        await runner.run(MyFlow())



def test_basic():
    client.run("...")

