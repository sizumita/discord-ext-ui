=====================
discord-ext-ui
=====================

.. image:: https://static.pepy.tech/personalized-badge/discord-ext-ui?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads
 :target: https://pepy.tech/project/discord-ext-ui
.. image:: https://img.shields.io/pypi/v/discord-ext-ui.svg
   :target: https://pypi.python.org/pypi/discord-ext-ui
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/discord-ext-ui.svg
   :target: https://pypi.python.org/pypi/discord-ext-ui
   :alt: PyPI supported Python versions

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
