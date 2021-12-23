# PaginationView, PageView

[サンプル](https://github.com/sizumita/discord-ext-ui/blob/master/samples/pagenation.py)

[カスタマイズのサンプル](https://github.com/sizumita/discord-ext-ui/blob/master/samples/custom_pagenation.py)

PaginationViewは、渡したPageViewをdiscord.ext.pagesのように遷移せることができます。

PageViewを継承し、body関数を変更してください。

```python
class Page(PageView):
    def __init__(self, content: str):
        super(Page, self).__init__()
        self.content = content

    async def body(self, _paginator: PaginationView) -> Message | View:
        return Message(self.content)
```

また、ページが遷移しページが表示されるとき、PageViewのon_appearが呼び出されます（引数が少し異なることに注意してください。）

```python
async def on_appear(self, paginator: PaginationView) -> None:
    print(f"appeared page: {paginator.page}")
```

子PageViewのなかで親PaginationViewのpage変数を変更すると、ページ遷移が可能です。

子PageViewでもボタンを使っている場合、ボタンは子PageViewのボタンの下に表示されます（PaginationViewによってボタンの個数が最大5個消費されることに注意してください。）

PaginationViewには下部に表示されるボタンの設定を変更できます。

- show_buttons
  - ボタンを表示するか
- show_disabled
  - 無効になっているボタンを表示するか
- show_indicator
  - 中央の`1/10`のようなページ番号を表示するか
- check
  - discord.Interactionを引数にとり、ボタンが押されたときに遷移するかどうかのチェック関数（押した人のフィルターなど）
- first_page
  - 最初に表示するページを設定します。デフォルトは0です
- cls 
  - ボタンの生成クラスを設定します(後述)。変更したい場合はdiscord.ext.ui.PaginationButtonsを継承してください

## ボタンの見た目を変える

PaginationButtonsを継承し、first, previous, indicator, next, last関数を編集しそれをPaginationViewのcls引数に渡してください。

```python
class CustomButtons(PaginationButtons):
    def first(self, now: int, last_page: int) -> Button:
        return Button("FIRST").style(discord.ButtonStyle.blurple)

    def last(self, now: int, last_page: int) -> Button:
        return Button("LAST").style(discord.ButtonStyle.blurple).disabled(now == last_page)

view = PaginationView(..., cls=CustomButtons)
```
