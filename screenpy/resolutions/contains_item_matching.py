"""
Matches a sequence which contains an item matching a given regex pattern.
"""

from .base_resolution import BaseResolution
from .custom_matchers.sequence_containing_pattern import (
    IsSequenceContainingPattern,
    has_item_matching,
)


class ContainsItemMatching(BaseResolution):
    """Match a sequence containing an item matching a regular expression.

    Examples::

        the_actor.should(
            # matches "Spam...", "Spam spam...", "Spam spam spam..."
            See.the(Text.of_all(MENU_ITEMS), ContainsItemMatching(r"^([Ss]pam ?)+"))
        )
    """

    matcher: IsSequenceContainingPattern
    line = 'a sequence with an item matching the regular expression "{expectation}".'
    matcher_function = has_item_matching

    def __init__(self, match: str) -> None:
        super().__init__(match)
