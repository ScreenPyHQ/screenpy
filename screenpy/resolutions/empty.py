from hamcrest import *

from .base_resolution import Resolution


class Empty(Resolution):
    """
    Matches on an empty collection (e.g. `[]`).
    """

    line = "for the collection to be empty"

    def __init__(self) -> None:
        self.expected = None
        self.matcher = empty()
