# インストール

```shell
$ pip install discord-ext-ui
```

# 基本的な使い方

```python
import discord
from discord.ext.ui import View, Message, Button, MessageProvider, ViewTracker


class MyView(View):
    async def body(self):
        return Message(
            content="here is content",
            components=[
                Button("love gura"),
                Button("love nizisanzi")
                .emoji("🌈")
                .disabled(True),
                Button("print a")
                .style(discord.ButtonStyle.secondary)
                .on_click(lambda x: print("a"))
            ]
        )

client = discord.Client()

...

await ViewTracker(MyView()).track(MessageProvider(channel))

```

discord.ext.uiのViewクラスを継承したクラスを作り、body関数でMessageを返してください。

Messageにはcontent、embed、componentを渡すことができます。
contentとembedはdiscord.Messageable.sendの仕様と同じです。

ComponentのitemsにはButtonとSelectを渡すことができます。

Buttonクラスにはdiscord.ui.Buttonに渡せる情報が渡せます。
この時、initに引数として渡すのと、関数に渡すのと、二つの方法を使うことができます。

on_click関数に関数を渡すと、
ボタンがクリックされたときに第一引数にdiscord.Interactionオブジェクトが渡されつつ実行されます。

コルーチン関数も、普通の関数も渡すことができます。適宜partialなどを使ってください。
こちらではinteraction_partialを用意しています（関数と引数を渡すと、第一引数にinteractionのオブジェクトを入れつつ実行してくれます。）

itemsに`list[Button, Button]`を渡すと、ボタンが５個詰めで並びます。
`list[list[Button],list[Button]]`を渡すと、段が分けられます。各段には５個までボタンを配置できます。

## state

discord-ext-uiはstateと言うプロパティを提供します。これを使っている変数が変更されたときに、自動でViewが更新されます。

```python
class MyView(View):
    something = state('something')
    def __init__(self):
        self.something = "what happened!?"

    def update_something(self):
        self.something = "nothing is happened."

    async def body(self):
        return Message(
            content=self.something,
            component=[Button("show").on_click(self.update_something)]
        )
```

showと言うボタンが押されたとき、self.somethingが変更されます。このとき、自動でviewが更新されます。

## discord.ext.commands.Botを使った際に使える機能

## ObservableObject

ObservableObjectを継承しているクラスのインスタンス変数をpublishedでラップすると、その変数が変更されたときに自動的にviewが更新されます。
