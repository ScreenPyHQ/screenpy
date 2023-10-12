"""Matches a value greater than the given number."""

from typing import Any

from hamcrest import greater_than_or_equal_to
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop


class IsGreaterThanOrEqualTo:
    """Match on a number that is greater than or equal to the given number.

    Examples::

        the_actor.should(
            See.the(Number.of(COUPONS), IsGreaterThanOrEqualTo(1))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Greater than or equal to {self.number_to_log}."

    @beat("... hoping it's greater than or equal to {number_to_log}.")
    def resolve(self) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        return greater_than_or_equal_to(self.number)

    def __init__(self, number: float) -> None:
        self.number = number
        self.number_to_log = represent_prop(number)
