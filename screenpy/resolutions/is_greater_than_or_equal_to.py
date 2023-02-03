"""
Matches a value greater than the given number.
"""

from typing import Union

from hamcrest import greater_than_or_equal_to
from hamcrest.library.number.ordering_comparison import OrderingComparison

from .base_resolution import BaseResolution


class IsGreaterThanOrEqualTo(BaseResolution):
    """Match on a number that is greater than or equal to the given number.

    Examples::

        the_actor.should(
            See.the(Number.of(COUPONS), IsGreaterThanOrEqualTo(1))
        )
    """

    matcher: OrderingComparison
    line = "greater than or equal to {expectation}"
    matcher_function = greater_than_or_equal_to

    def __init__(self, number: Union[int, float]) -> None:
        super().__init__(number)
