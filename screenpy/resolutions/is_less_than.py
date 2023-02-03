"""
Matches a value less than the given number.
"""

from typing import Union

from hamcrest import less_than
from hamcrest.library.number.ordering_comparison import OrderingComparison

from .base_resolution import BaseResolution


class IsLessThan(BaseResolution):
    """Match on a number that is less than the given number.

    Examples::

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_POPUPS), IsLessThan(1))
        )
    """

    matcher: OrderingComparison
    line = "less than {expectation}"
    matcher_function = less_than

    def __init__(self, number: Union[int, float]) -> None:
        super().__init__(number)
