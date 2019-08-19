from hamcrest import *

from .base_resolution import Resolution


class ContainsTheText(Resolution):
    """
    Matches a substring (e.g. `"play" in "screenplay"`).
    """

    line = "to have '{}'"

    def __init__(self, substring: str) -> None:
        self.expected = substring
        self.matcher = contains_string(substring)
