"""
A resolution that matches against the length of a collection.
"""

from typing import Sized

from hamcrest import has_length
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class HasLength(BaseResolution):
    """Match against a collection with a specific length.

    Examples::

        the_actor.should_see_the(
            (Selected.options_from(INDUSTRIES), HasLength(5))
        )
    """

    expected: int
    matcher: Matcher[Sized]

    line = "a collection with {expectation} items in it"

    def __init__(self, length: int) -> None:
        self.expected = length
        self.matcher = has_length(length)
