"""
ReadsExactly an exact string.
"""

from typing import TypeVar

from hamcrest import has_string
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

SelfReadsExactly = TypeVar("SelfReadsExactly", bound="ReadsExactly")


class ReadsExactly:
    """Match a specific string exactly.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_MESSAGE), ReadsExactly("Log in below."))
        )
    """

    def describe(self: SelfReadsExactly) -> str:
        """Describe the Resolution's expectation."""
        return f'"{self.text}", verbatim.'

    @beat('... hoping it\'s "{text}", verbatim.')
    def resolve(self: SelfReadsExactly) -> Matcher[object]:
        """Produce the Matcher to make the assertion."""
        return has_string(self.text)

    def __init__(self, text: str) -> None:
        self.text = text
