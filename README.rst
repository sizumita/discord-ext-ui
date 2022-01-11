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

This package is an extension of discord.ui.

You can use pycord or discord.py.

I hate pycord's slash command system.

why use discord-ext-ui?
=============================

discord-ext-ui comes with a declarative View system and Combine system similar to SwiftUI.

This makes it easier to implement architectures such as MVVM and to edit buttons after they have been submitted.

Advantages of adopting discord-ext-ui
-------------------------------------

1. no more need to explicitly update the message

As an example, let's say you want to implement a function that allows you to increase or decrease the count using a button.

If you want to implement it without using MVVM, you need to explicitly write a process to update the message to reflect the change in the internal state when the button is pressed.

On the other hand, discord-ext-ui provides wrappers for variables such as `state` and `published`. By using this wrapper, it is not necessary to explicitly write message updates according to changes in member variables.

Also, since the function to be executed when the button is pressed can be set declaratively, it is possible to perform complex processing such as for loops. 2.

2. easy to write when a button is used

With discord-ext-ui, it is possible to change buttons when updating automatically, so it is easy to implement disabling/enabling according to instance variable values and changing buttons according to internal states such as pagination.

Example
=======

See `./examples/`.

.. code-block::python
    from discord.ext.ui import Button, View, ObservableObject, published, Message, ViewTracker, MessageProvider
    from discord.ext.ui.combine import PassThroughSubject
    import discord
    import os


    client = discord.Client()


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

        async def delete(self, interaction: discord.Interaction):
            await interaction.message.delete()
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
                        .on_click(self.delete)
                        .style(discord.ButtonStyle.danger)
                ]
            ])


    @client.event
    async def on_message(message: discord.Message):
        if message.content != "!test":
            return

        view = SampleView()
        tracker = ViewTracker(view, timeout=None)
        await tracker.track(MessageProvider(message.channel))

LICENSE
=======

MIT
