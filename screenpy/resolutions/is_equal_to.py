from hamcrest import *

from .base_resolution import Resolution


class IsEqualTo(Resolution):
    """
    Matches on equality (i.e. `a == b`).
    """

    line = "to find {}"

    def __init__(self, obj: object) -> None:
        self.expected = obj
        self.matcher = equal_to(obj)
