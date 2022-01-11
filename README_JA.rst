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

このパッケージはdiscord.uiの拡張です。

why use discord-ext-ui ? なぜdiscord-ext-uiを使うのか?
=============================

discord-ext-uiは、SwiftUIに似た宣言的Viewシステム・Combineシステムを搭載しています。

これにより、MVVMなどのアーキテクチャを実装したり、送信した後のボタンの編集が容易になります。

discord-ext-uiを採用する利点
-----------------------------

1.	メッセージの更新を明示的に行う必要がなくなる

例として、ボタンを使ってカウントを増やしたり減らしたりできるような機能を実装するとしましょう。

MVVMを用いらずに実装する場合、ボタンの押下時に内部状態が変更された際にその状態を反映してメッセージの更新を行う処理を明示的に記述する必要があります。

対して、discord-ext-uiでは、 `state` や `published` といった変数のラッパーを提供します。このラッパーを使用することで、メンバ変数の変更に応じてメッセージの更新を明示的に書く必要がなくなります。

また、ボタンが押されたときに実行される関数を宣言的に設定できるので、forループ等の複雑な処理を行うことも可能です。

2.	ボタンを使った時の処理が書きやすい

discord-ext-uiを使えば、自動で更新する際にボタンの変更も可能なので、インスタンス変数の値に応じた無効化・有効化や、ペジネーション等の内部状態に応じたボタンの変更処理も簡単に実装することができます。

Example
=======

`./examples/` をご覧ください。

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
