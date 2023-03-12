"""
Matches a sequence which contains an item matching a given regex pattern.
"""

from typing import Sequence, TypeVar

from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

from .custom_matchers.sequence_containing_pattern import has_item_matching

SelfContainsItemMatching = TypeVar(
    "SelfContainsItemMatching", bound="ContainsItemMatching"
)


class ContainsItemMatching:
    """Match a sequence containing an item matching a regular expression.

    Examples::

        the_actor.should(
            # matches "Spam...", "Spam spam...", "Spam spam spam..."
            See.the(Text.of_all(MENU_ITEMS), ContainsItemMatching(r"^([Ss]pam ?)+"))
        )
    """

    def describe(self: SelfContainsItemMatching) -> str:
        """Describe the Resolution in present tense."""
        return f"Match the pattern {self.pattern}."

    @beat('... hoping it contains an item matching the pattern "{pattern}".')
    def resolve(self: SelfContainsItemMatching) -> Matcher[Sequence[str]]:
        """Produce the Matcher to make the assertion."""
        return has_item_matching(self.pattern)

    def __init__(self: SelfContainsItemMatching, pattern: str) -> None:
        self.pattern = pattern
