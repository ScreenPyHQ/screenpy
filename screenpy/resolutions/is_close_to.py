"""Matches a value that falls within a range specified by the given delta."""

from hamcrest import close_to
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop


class IsCloseTo:
    """Matches a value that falls within the range specified by the given delta.

    Examples::

        the_actor.should(
            See.the(Number.of(BALLOONS), IsCloseTo(FILLED_BALLOONS_COUNT, delta=25))
        )
    """

    @property
    def delta_to_log(self) -> str:
        """Represent the delta in a log-friendly way."""
        return represent_prop(self.delta)

    @property
    def num_to_log(self) -> str:
        """Represent the num in a log-friendly way."""
        return represent_prop(self.num)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"At most {self.delta_to_log} away from {self.num_to_log}."

    @beat("... hoping it's at most {delta_to_log} away from {num_to_log}.")
    def resolve(self) -> Matcher[float]:
        """Produce the Matcher to make the assertion."""
        return close_to(self.num, self.delta)

    def __init__(self, num: int, delta: int = 1) -> None:
        self.num = num
        self.delta = delta
