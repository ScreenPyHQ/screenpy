from screenpy import Director


def test_is_singleton() -> None:
    d1 = Director()
    d2 = Director()

    assert d1 is d2
