"""Matches a string using a regex pattern."""

from __future__ import annotations

from re import Pattern
from typing import TYPE_CHECKING

from hamcrest import matches_regexp

from screenpy.pacing import beat

if TYPE_CHECKING:  # pragma: no cover
    from hamcrest.core.matcher import Matcher


class Matches:
    """Match a string using a regular expression.

    Examples::

        the_actor.should(
            # matches "/product/1", "/product/22", "/product/942"...
            See.the(Text.of_the(URL), Matches(r"/product/[0-9]{1,3}"))
        )

        # matches "/people/123/edit", "/people/2ec4efef-dec5-9d81bbcc410a/edit"
        pattern = re.compile(r"/people/.+/edit")
        the_actor.should(See.the(Text.of_the(URL), Matches(pattern))

    """

    @property
    def pattern_to_log(self) -> str:
        """Represent the item in a log-friendly way."""
        if isinstance(self.pattern, Pattern):
            return f"r'{self.pattern.pattern}'"
        return f"r'{self.pattern}'"

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Text matching the pattern {self.pattern_to_log}."

    @beat("... hoping it's text matching the pattern {pattern_to_log}.")
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return matches_regexp(self.pattern)

    def __init__(self, pattern: str | Pattern[str]) -> None:
        self.pattern = pattern
