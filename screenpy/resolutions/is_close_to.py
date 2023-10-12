"""Matches a value that falls within a range specified by the given delta."""

from hamcrest import close_to
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class IsCloseTo:
    """Matches a value that falls within the range specified by the given delta.

    Examples::

        the_actor.should(
            See.the(Number.of(BALLOONS), IsCloseTo(FILLED_BALLOONS_COUNT, delta=25))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"At most {self.delta} away from {self.num}."

    @beat("... hoping it's at most {delta} away from {num}.")
    def resolve(self) -> Matcher[float]:
        """Produce the Matcher to make the assertion."""
        return close_to(self.num, self.delta)

    def __init__(self, num: int, delta: int = 1) -> None:
        self.num = num
        self.delta = delta
