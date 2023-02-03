"""
Matches a value less than or equal to the given number.
"""

from typing import Union

from hamcrest import less_than_or_equal_to
from hamcrest.library.number.ordering_comparison import OrderingComparison

from .base_resolution import BaseResolution


class IsLessThanOrEqualTo(BaseResolution):
    """Match on a number that is less than or equal to the given number.

    Examples::

        the_actor.should(
            See.the(Number.of(VOUCHER_INPUTS), IsLessThanOrEqualTo(1))
        )
    """

    matcher: OrderingComparison
    line = "less than or equal to {expectation}"
    matcher_function = less_than_or_equal_to

    def __init__(self, number: Union[int, float]) -> None:
        super().__init__(number)
