"""
Matches using equality.
"""

from typing import Any

from hamcrest import equal_to
from hamcrest.core.core.isequal import IsEqual

from .base_resolution import BaseResolution


class IsEqualTo(BaseResolution):
    """Match on an equal object.

    Examples::

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0))
        )
    """

    matcher: IsEqual
    line = "equal to {expectation}"
    matcher_function = equal_to

    def __init__(self, obj: Any) -> None:
        super().__init__(obj)
