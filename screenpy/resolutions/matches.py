"""Matches a string using a regex pattern."""

from hamcrest import matches_regexp
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class Matches:
    """Match a string using a regular expression.

    Examples::

        the_actor.should(
            # matches "/product/1", "/product/22", "/product/942"...
            See.the(Text.of_the(URL), Matches(r"/product/[0-9]{1,3}"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f'Text matching the pattern r"{self.pattern}".'

    @beat('... hoping it\'s text matching the pattern r"{pattern}".')
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return matches_regexp(self.pattern)

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
