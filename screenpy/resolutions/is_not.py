from hamcrest import *

from .base_resolution import Resolution


class IsNot(Resolution):
    """
    Matches a negated Resolution (e.g. `not ReadsExactly("yes")`).
    """

    line = "not {}"

    def __init__(self, resolution: "Resolution") -> None:
        self.expected = resolution
        self.matcher = is_not(resolution)
