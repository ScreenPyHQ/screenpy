"""Matches a value greater than the given number."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from hamcrest import greater_than

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

if TYPE_CHECKING:
    from hamcrest.core.matcher import Matcher


class IsGreaterThan:
    """Match on a number that is greater than the given number.

    Examples::

        the_actor.should(See.the(Number.of(COUPONS), IsGreaterThan(1)))
    """

    @property
    def number_to_log(self) -> str | float:
        """Represent the number in a log-friendly way."""
        return represent_prop(self.number)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Greater than {self.number_to_log}."

    @beat("... hoping it's greater than {number_to_log}.")
    def resolve(self) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        return greater_than(self.number)

    def __init__(self, number: float) -> None:
        self.number = number
