"""
Matches a number against a range.
"""

from typing import Union

from .base_resolution import BaseResolution
from .custom_matchers.is_in_bounds import IsInBounds, is_in_bounds


class IsInRange(BaseResolution):
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

    matcher: IsInBounds
    line = "in the range {expectation}"
    matcher_function = is_in_bounds

    def __init__(self, *bounds: Union[int, str]) -> None:
        super().__init__(*bounds)
