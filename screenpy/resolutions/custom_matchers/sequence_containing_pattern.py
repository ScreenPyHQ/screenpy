"""Matcher to use a regular expression pattern to match an item in a sequence."""

import re
from typing import Sequence

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher


class IsSequenceContainingPattern(BaseMatcher[Sequence[str]]):
    """Matcher to test each string in a sequence against a regex."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def _matches(self, item: Sequence[str]) -> bool:
        try:
            for element in item:
                if re.match(self.pattern, element):
                    return True
        except TypeError:  # not a sequence
            pass
        return False

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text(
            f'a sequence containing an element which matches r"{self.pattern}"'
        )

    def describe_match(self, _: Sequence[str], match_description: Description) -> None:
        """Describe the match, for use with IsNot."""
        match_description.append_text(f'it contains an item matching "{self.pattern}"')

    def describe_mismatch(
        self, item: Sequence[str], mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        if item is None or not hasattr(item, "__iter__"):
            mismatch_description.append_text("was not a sequence")
            return
        mismatch_description.append_text(
            f'did not contain an item matching r"{self.pattern}"'
        )


def has_item_matching(pattern: str) -> Matcher[Sequence[str]]:
    """Matches if any element of sequence matches the regex pattern."""
    return IsSequenceContainingPattern(pattern)
