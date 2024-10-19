import discord

import sys

sys.path.append("discord")
from ext.ui import Runner, RunnerPool, Flow, Signal, DiscordProvider, Context, View, state, Button, ViewMessage


class MyView(View[Signal, DiscordProvider]):
    value = state(0)

    async def callback(self, c: Context[Signal], interaction: discord.Interaction,
                       item: discord.ui.Button) -> Signal | None:
        print(self.value)
        self.value += 1
        await interaction.response.send_message("ok")
        return None

    async def callback2(self, c: Context[Signal], interaction: discord.Interaction,
                        item: discord.ui.Button) -> Signal | None:
        print(item)
        return Signal("ok")

    async def render(self, ctx: Context[DiscordProvider]) -> ViewMessage[Signal, DiscordProvider]:
        return ViewMessage(
            content=f"{self.value}",
            elements=[
                [
                    Button(label="test")
                    .on_click(self.callback),
                    Button(label="finish")
                    .on_click(self.callback2)
                ]
            ]
        )


class MyFlow(Flow[Signal, DiscordProvider]):
    async def run(self, ctx: Context[DiscordProvider]) -> Signal:
        finish = await ctx.checkpoint(MyView()).display()

        return Signal("name")


client = discord.Client(intents=discord.Intents.all())
pool = RunnerPool()


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content == "abc":
        provider = DiscordProvider(client, message.channel)
        runner = Runner(provider)
        pool.register(runner)
        await runner.run(MyFlow())


if __name__ == '__main__':
    client.run("...")
