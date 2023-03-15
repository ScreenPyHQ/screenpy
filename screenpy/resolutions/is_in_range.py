"""
Matches a number against a range.
"""

from typing import Union

from hamcrest.core.matcher import Matcher

from screenpy.exceptions import UnableToFormResolution
from screenpy.pacing import beat

from .custom_matchers.is_in_bounds import is_in_bounds


class IsInRange:
    """Match on a number within a given range.

    By default, this Resolution assumes an inclusive range (i.e. [x, y])
    if no brackets are used in the range string or if numbers are used.

    Examples::

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_BANNERS), IsInRange(1, 5))
        )

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_BANNERS), IsInRange("(1, 5)"))
        )

        the_actor.should(See.the(Number.of(PUPPY_PICTURES), IsInRange("1-5")))

        the_actor.should(See.the(Number.of(COOKIES), IsInRange("[1, 5)")))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"In the range {self.bounding_string}."

    @beat("... hoping it's in the range {bounding_string}.")
    def resolve(self) -> Matcher[float]:
        """Produce the Matcher to make the assertion."""
        return is_in_bounds(*self.bounds)

    def __init__(self, *bounds: Union[int, str]) -> None:
        if len(bounds) > 2:
            msg = f"{self.__class__.__name__} was given too many arguments: {bounds}."
            raise UnableToFormResolution(msg)

        self.bounds = bounds
        self.bounding_string = self.bounds[0]  # given bounding string
        if len(self.bounds) == 2:
            # given bounding numbers
            self.bounding_string = f"[{self.bounds[0]}, {self.bounds[1]}]"
