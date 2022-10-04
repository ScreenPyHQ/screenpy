from screenpy import __version__


def test_metadata() -> None:
    assert __version__.__title__ == "screenpy"
    assert __version__.__license__ == "MIT"
    assert __version__.__author__ == "Perry Goy"
