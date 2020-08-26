"""
A resolution that matches using equality.
"""

from typing import Any, Optional

from hamcrest import equal_to
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class IsEqualTo(BaseResolution):
    """Match on an equal object.

    Examples::

        the_actor.should_see_the(
            (Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0))
        )

        the_actor.should_see_the(
            (Text.of_all(SEARCH_RESULTS), IsEqualTo(["R2-D2", "C-3PO"])))
    """

    expected: object
    matcher: Matcher[Optional[Any]]

    line = "equal to {expectation}"

    def __init__(self, obj: object) -> None:
        self.expected = obj
        self.matcher = equal_to(obj)
