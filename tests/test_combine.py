from discord.ext.ui.combine import Just, PassThroughSubject


def assert_two(x, y):
    assert x == y


def test_just_1():
    Just(1).sink(lambda x: assert_two(x, 1))


def test_just_2():
    Just(2).map(lambda x: x * 2).sink(lambda x: assert_two(x, 4))


def test_subject_1():
    sub = PassThroughSubject()
    sub.sink(lambda x: assert_two(x, 1)).send(1)
