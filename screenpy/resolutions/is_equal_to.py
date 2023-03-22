"""
Matches using equality.
"""

from typing import Any

from hamcrest import equal_to
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class IsEqualTo:
    """Match on an equal object.

    Examples::

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Equal to {self.expected}."

    @beat("... hoping it's equal to {expected}.")
    def resolve(self) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        return equal_to(self.expected)

    def __init__(self, obj: Any) -> None:
        self.expected = obj
