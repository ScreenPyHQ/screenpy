from hamcrest import *

from .base_resolution import Resolution


class ReadsExactly(Resolution):
    """
    Matches a string exactly (e.g. `"screenplay" == "screenplay"`).
    """

    line = "to read '{},' exactly"

    def __init__(self, string: str) -> None:
        self.expected = string
        self.matcher = has_string(string)
