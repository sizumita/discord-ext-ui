# 2.0 変更点

## StateとPublished

1.xではState(value)のように記述していましたが、2.0以降はクラス変数のように使います。

Before:

```python
class MyView(View):
    def __init__(self, bot):
        super().__init__(bot)
        self.something = State(1)

```

After:

```python
class MyView(View):
    something = state("something")

    def __init__(self, bot):
        super().__init__(bot)
        self.something = 1

```

クラス変数のように見えますが、プロパティであるためそれぞれのインスタンス毎に違う値を持ちます。また、`state`の引数はstateが保存される実変数名になります。

Publishedも同じように変更されます。

## View.get_message()

View.get_message()はView.messageに変更されます。

## ViewBuilderの追加

Viewを簡単に作成できる、ViewBuilderが追加されます。使い方については`samples/view_builder.py` をご覧ください。
