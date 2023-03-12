"""
Matches a value greater than the given number.
"""

from typing import Any, TypeVar

from hamcrest import greater_than
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

SelfIsGreaterThan = TypeVar("SelfIsGreaterThan", bound="IsGreaterThan")


class IsGreaterThan:
    """Match on a number that is greater than the given number.

    Examples::

        the_actor.should(See.the(Number.of(COUPONS), IsGreaterThan(1)))
    """

    def describe(self: SelfIsGreaterThan) -> str:
        """Describe the Resolution's expectation."""
        return f"Greater than {self.number}."

    @beat("... hoping it's greater than {number}.")
    def resolve(self: SelfIsGreaterThan) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        return greater_than(self.number)

    def __init__(self, number: float) -> None:
        self.number = number
