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

MVVMアーキテクチャを採用する利点
-----------------------

まずMVVMとは、各クラスが公開インスタンス変数を管理することによって、画面状態の管理を安全に行うことのできるModel View ViewModelと呼ばれるアーキテクチャの略称です。

MVVMにおいてコンポーネントの設計はView、ViewModel、Modelにわけられ、それぞれ別の役割を担います。

https://qiita.com/yuutetu/items/ea175b73e1dbbfd355db

詳しくはこちらなどの記事を参考にしてください。

MVVMにより、ロジック部分と画面への描画部分、およびDiscordへの通信部分が分けられるため、ロジックに対するテストが書きやすく、結果として品質の高いコードを維持することができます。

discord-ext-uiを採用する利点
-------------------------

1.	メッセージの更新を明示的に行う必要がなくなる

例として、ボタンを使ってカウントを増やしたり減らしたりできるような機能を実装するとしましょう。

MVVMを用いらずに実装する場合、ボタンの押下時に内部状態が変更された際にその状態を反映してメッセージの更新を行う処理を明示的に記述する必要があります。

対して、discord-ext-uiでは、 `State` や `Published` といった変数のラッパーを提供します。このラッパーを使用することで、メンバ変数の変更に応じてメッセージの更新を明示的に書く必要がなくなります。

また、ボタンが押されたときに実行される関数を宣言的に設定できるので、forループ等の複雑な処理を行うことも可能です。

2.	ボタンを使った時の処理が書きやすい

discord.py 2.0からボタンの対応が始まりましたが、discord.py標準のボタン対応の仕組みでは、途中でボタンの変更などがし辛いなどの問題があります。

discord-ext-uiを使えば、自動で更新する際にボタンの変更も可能なので、インスタンス変数の値に応じた無効化・有効化や、ペジネーション等の内部状態に応じたボタンの変更処理も簡単に実装することができます。

discord-ext-uiの概念
==================

discord-ext-uiは宣言的なUIを実装するためのフレームワークです。
このパッケージは特にSwiftUIの影響を受けていてそれに由来する4つの概念を持っています。

View
====

Viewは `body` という名前のメソッドを実装しなければなりません。
`body` メソッドはdiscord-ext-uiの `Message` を返却する必要があります。
ライブラリは `body` メソッドをメッセージを作成/更新する際に毎回呼び出し、その結果を用いてDiscord APIを呼び出します。
`View` クラスは `start` メソッドを持っていて、これにチャンネルを渡すことでメッセージの作成が行われます。

State
=====

StateはViewのインスタンス変数として使います。
View上のStateを更新するとメッセージの更新が行われます。つまり、ライブラリによって、 `body` メソッドが呼び出され、その結果を用いてDiscord上のメッセージが更新されます。

ObservedObjectとPublished
=========================

これはMVVMに関連した概念です。MVVMを用いないのであればこの節は読まなくても良いかもしれません。
`ObservedObject` を継承したViewModelをViewのインスタンス変数とするとViewは自動的にViewModelの `Published` クラスのインスタンスである変数の変更を監視します。
ViewModelの `Published` クラスのインスタンスである変数の変更が行われるとStateの更新時と同じようにメッセージの更新が行われます。(データバインディング)


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
