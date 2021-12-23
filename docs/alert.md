# Alert

Alertはボタン付きのViewを表示し、ボタンを押された場合にボタンに紐ついている値を返します。

サンプルはこちら: https://github.com/sizumita/discord-ext-ui/blob/master/samples/alert.py

```python
import discord

from discord.ext.ui import Alert, ActionButton

alert = Alert("編集を終了しますか？", "", [
    ActionButton("いいえ", discord.ButtonStyle.blurple, value=False),
    ActionButton("はい", discord.ButtonStyle.danger, value=True)
], ephemeral=True)
```

Alertにはtitle, text, ボタンを設定できます。ボタンはActionButtonのみ対応しています。

keyword argumentsを渡すことでinteraction.response.send_messageなどの引数を追加できます。

```python
await alert.wait_for_click(interaction)
```

を使って送信し、ActionButtonに設定したvalueを返します。

Alertの画面を編集したい場合はAlertを継承したclassのbody関数を変更してください。
