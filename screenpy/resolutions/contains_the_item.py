"""
A resolution that matches against a list that contains the desired item.
"""

from typing import Any, Sequence

from hamcrest import has_item
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheItem(BaseResolution):
    """Match an iterable containing a specific item.

    Examples::

        the_actor.should_see_the(
            (Text.of_all(SEARCH_RESULTS), ContainsTheItem("The Droids"))
        )
    """

    expected: object
    matcher: Matcher[Sequence[Any]]

    line = 'list containing the item "{expectation}"'

    def __init__(self, item: object) -> None:
        self.expected = str(item)
        self.matcher = has_item(item)
