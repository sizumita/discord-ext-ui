# インストール

```shell
$ pip install discord-ext-ui
```

# 基本的な使い方

```python
import discord
from discord.ext.ui import View, Message, Component, Button


class MyView(View):
    async def body(self):
        return Message(
            content="here is content",
            component=Component(
                items=[
                    Button("love gura"),
                    Button("love nizisanzi")
                    .emoji("🌈")
                    .disabled(True),
                    Button("print a")
                    .style(discord.ButtonStyle.secondary)
                    .on_click(lambda x: print("a"))
                ]
            )
        ).on_appear(lambda: print("appear view"))\
        .on_disappear(lambda: print("disappear view"))

client = discord.Client()

...

await MyView(client).start(some_text_channel)

```

discord.ext.uiのViewクラスを継承したクラスを作り、body関数でMessageを返してください。

Messageにはcontent、embed、componentを渡すことができます。
contentとembedはdiscord.Messageable.sendの仕様と同じです。

ComponentのitemsにはButton(将来的にはselectも)を渡すことができます。

Buttonクラスにはdiscord.ui.Buttonに渡せる情報が渡せます。
この時、initに引数として渡すのと、関数に渡すのと、二つの方法を使うことができます。

on_click関数に関数を渡すと、
ボタンがクリックされたときに第一引数にdiscord.Interactionオブジェクトが渡されつつ実行されます。

コルーチン関数も、普通の関数も渡すことができます。適宜partialなどを使ってください。
こちらではinteraction_partialを用意しています（関数と引数を渡すと、第一引数にinteractionのオブジェクトを入れつつ実行してくれます。）

itemsに`list[Button, Button]`を渡すと、ボタンが５個詰めで並びます。
`list[list[Button],list[Button]]`を渡すと、段が分けられます。各段には５個までボタンを配置できます。

Messageにはon_appear,on_disappearが存在し、これらはそれぞれView.start関数、View.stop関数が実行された際に呼び出されます。
引数なしの関数またはコルーチン関数を渡してください。

## discord.ext.commands.Botを使った際に使える機能

### discordのイベントリスナー

commands.Cog.listener()デコレータと同じように、デコレーターを使ってdiscordのイベントを受け取ることができます:

```python
class MyView(View):
    @View.listen()
    async def on_message(self, message):
        ...
```

## ObservedObject

ObservedObjectを継承しているクラスのインスタンス変数をPublishedでラップすると、その変数が変更されたときに自動的にviewが更新されます。
