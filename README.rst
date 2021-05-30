=====================
discord-ext-ui
=====================

This package is extension of discord.ui.

You can build ui like SwiftUI.

Features
========

View System
-----------

You can build UI by View class.

View.body function returns what you want to show.

Combine System
--------------

You can use Combine like Swift's Combine.


Example
=======

.. code-block:: python
    from discord.ext.ui import Component, Button, View, ObservedObject, Published, Message
    from discord.ext import commands
    import discord
    import os

    client = commands.Bot("!")


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

        async def add_reaction(self):
            await self.discord_message.add_reaction("\U0001f44d")

        async def body(self):
            return Message(
                content=f"test! {self.viewModel.num}",
                component=Component(items=[
                    [
                        Button("+1")
                            .on_click(lambda x: self.viewModel.countup())
                            .style(discord.ButtonStyle.blurple),

                        Button("-1")
                            .on_click(lambda x: self.viewModel.countdown())
                            .style(discord.ButtonStyle.blurple)
                    ]
                ])
            )


    @client.event
    async def on_message(message):
        if message.content != "!test":
            return
        await SampleView().start(client, message.channel)
