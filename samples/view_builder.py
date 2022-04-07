import os

import discord
from discord.ext.ui import ViewBuilder, Button
from discord.ext import commands


bot = commands.Bot("!", intents=discord.Intents.default())


@bot.command()
async def button(ctx: commands.Context):
    builder = ViewBuilder()
    builder.append(
        Button("don't click me!")
        .style(discord.ButtonStyle.danger)
        .on_click(lambda x: print("bomb!"))
    )
    await ctx.send("here is danger button", view=builder.build())

bot.run(os.environ["DISCORD_BOT_TOKEN"])
