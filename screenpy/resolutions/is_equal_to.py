"""
Matches using equality.
"""

from typing import Any, TypeVar

from hamcrest import equal_to
from hamcrest.core.base_matcher import Matcher

from screenpy.pacing import beat

SelfIsEqualTo = TypeVar("SelfIsEqualTo", bound="IsEqualTo")


class IsEqualTo:
    """Match on an equal object.

    Examples::

        the_actor.should(
            See.the(Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0))
        )
    """

    @beat("... hoping it's equal to {expected}.")
    def resolve(self: SelfIsEqualTo) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        return equal_to(self.expected)

    def __init__(self: SelfIsEqualTo, obj: Any) -> None:
        self.expected = obj
