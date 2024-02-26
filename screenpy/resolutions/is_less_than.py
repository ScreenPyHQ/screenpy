"""Matches a value less than the given number."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hamcrest import less_than

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

if TYPE_CHECKING:
    from hamcrest.core.matcher import Matcher


class IsLessThan:
    """Match on a number that is less than the given number.

    Examples::

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_POPUPS), IsLessThan(1))
        )
    """

    @property
    def number_to_log(self) -> str | float:
        """Represent the number in a log-friendly way."""
        return represent_prop(self.number)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Less than {self.number_to_log}."

    @beat("... hoping it's less than {number_to_log}.")
    def resolve(self) -> Matcher[float]:
        """Produce the Matcher to make the assertion."""
        return less_than(self.number)

    def __init__(self, number: float) -> None:
        self.number = number
