"""
Matches a list that contains the desired item.
"""

from typing import TypeVar

from hamcrest import has_item
from hamcrest.library.collection.issequence_containing import IsSequenceContaining

from .base_resolution import BaseResolution

T = TypeVar("T")


class ContainsTheItem(BaseResolution):
    """Match an iterable containing a specific item.

    Examples::

        the_actor.should(
            See.the(Text.of_all(SEARCH_RESULTS), ContainsTheItem("The Droids"))
        )
    """

    matcher: IsSequenceContaining
    line = 'a list containing the item "{expectation}"'
    matcher_function = has_item

    def __init__(self, match: T) -> None:
        super().__init__(match)
