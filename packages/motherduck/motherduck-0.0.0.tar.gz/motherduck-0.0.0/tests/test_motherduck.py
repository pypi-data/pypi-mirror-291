from motherduck import say_quack


def test_say_quack():
    assert say_quack(2) == "quack quack"
