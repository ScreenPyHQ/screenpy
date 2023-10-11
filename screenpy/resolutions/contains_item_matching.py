"""Matches a sequence which contains an item matching a given regex pattern."""

from typing import Sequence

from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

from .custom_matchers.sequence_containing_pattern import has_item_matching


class ContainsItemMatching:
    """Match a sequence containing an item matching a regular expression.

    Examples::

        the_actor.should(
            # matches "Spam...", "Spam spam...", "Spam spam spam..."
            See.the(Text.of_all(MENU_ITEMS), ContainsItemMatching(r"^([Ss]pam ?)+"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f'A sequence with an item matching the pattern r"{self.pattern}".'

    @beat('... hoping it contains an item matching the pattern r"{pattern}".')
    def resolve(self) -> Matcher[Sequence[str]]:
        """Produce the Matcher to make the assertion."""
        return has_item_matching(self.pattern)

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
