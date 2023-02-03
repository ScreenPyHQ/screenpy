"""
Matches a value greater than the given number.
"""

from typing import Union

from hamcrest import greater_than
from hamcrest.library.number.ordering_comparison import OrderingComparison

from .base_resolution import BaseResolution


class IsGreaterThan(BaseResolution):
    """Match on a number that is greater than the given number.

    Examples::

        the_actor.should(See.the(Number.of(COUPONS), IsGreaterThan(1)))
    """

    matcher: OrderingComparison
    line = "greater than {expectation}"
    matcher_function = greater_than

    def __init__(self, number: Union[int, float]) -> None:
        super().__init__(number)
