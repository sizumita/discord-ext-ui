from discord.ext.ui.combine import Just, PassThroughSubject


if __name__ == '__main__':
    sub = PassThroughSubject()
    sub.map(lambda x: x * 5).sink(print)
    sub.send(1)
    # 5
    sub.send(2)
    # 10
    sub.send(3)
    # 15

    Just([1, 2, 3]).map(lambda x: x ** 2).sink(print)
    # [1, 4, 9]
