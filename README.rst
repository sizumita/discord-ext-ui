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

なぜdiscord-ext-uiを使うのか?
==========================

discord-ext-uiは、SwiftUIに似た宣言的Viewシステム・Combineシステムを搭載しています。

これにより、MVVMなどのアーキテクチャを実装したり、送信した後のボタンの編集が容易になります。

アーキテクチャを採用する利点
-----------------------

MVVMを参考にお話しします。

MVVMとは、各クラスが公開インスタンス変数を管理することによって、画面状態の管理を安全に行うアーキテクチャです。

View, ViewModel, Modelにわけ、それぞれに別の役割があります。

https://qiita.com/yuutetu/items/ea175b73e1dbbfd355db

こちらなどの記事を参考にしてください。

MVVMを使うと、実装方針が統一化され、品質の高いコードを維持できます。
また、ロジック（ビジネスロジック・プレゼンテーションロジック）を分けることができます。
また、ロジックが分かれているため、discordと通信する箇所を分けることができるので、テストが書けるようになります。

discord-ext-uiを採用する利点
-------------------------

明示的でないUIの更新ができる
^^^^^^^^^^^^^^^^^^^^^^^

Discordに表示される内容を作成するとき、今までは明示的に `Messageable.send` 関数などを使う必要がありましたが、discord-ext-uiを使うとその必要がなくなります。

数字のカウンターがあり、ボタンを押して増やしたり減らしたりできるとしましょう。

普通に作る場合、ボタンが押されたときに毎回アップデートする関数を明示的に実行する必要があります。

しかし、discord-ext-uiを使用すると、カウンターの変数を `State` または `Published` でラップすることで、その変数を変更した場合に自動的に更新されます！

また、ボタンが押されたときに実行される関数を宣言的に設定できるので、for文を使うことができます。

ボタンを使った時の処理が書きやすい
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

discord.py 2.0からボタンの対応が始まりましたが、discord.py標準のボタン対応の仕組みでは、途中でボタンの変更などがし辛いなどの問題があります。

ですが、discord-ext-uiを使えば、自動で更新する際にボタンも変更が可能なので、インスタンス変数の値によって無効・有効したり、ペジネーションを簡単に実装できます。

Example
=======

.. code-block:: python

    from discord.ext.ui import Component, Button, View, ObservedObject, Published, Message
    from discord.ext import commands
    import discord
    import os

    client = discord.Client()


    class SampleViewModel(ObservedObject):
        def __init__(self, bot):
            super().__init__(bot)
            self.num = Published(0)

        def countup(self):
            self.num += 1

        def countdown(self):
            self.num -= 1


    class SampleView(View):
        def __init__(self):
            super().__init__()
            self.view_model = SampleViewModel()

        async def add_reaction(self):
            await self.get_message().add_reaction("\U0001f44d")

        async def body(self):
            return Message(
                content=f"test! {self.view_model.num}",
                component=Component(items=[
                    [
                        Button("+1")
                            .on_click(lambda x: self.view_model.countup())
                            .style(discord.ButtonStyle.blurple),

                        Button("-1")
                            .on_click(lambda x: self.view_model.countdown())
                            .style(discord.ButtonStyle.blurple)
                    ]
                ])
            )


    @client.event
    async def on_message(message):
        if message.content != "!test":
            return
        await SampleView(client).start(message.channel)
