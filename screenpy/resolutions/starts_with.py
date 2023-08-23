"""
Matches a string which begins with a substring.
"""

from hamcrest import starts_with
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import tostring


class StartsWith:
    """Match a string which starts with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), StartsWith("Welcome"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Starting with {tostring(self.prefix)}."

    @property
    def beatmsg(self) -> str:
        """format string meant for beat msg"""
        return f"... hoping it starts with {tostring(self.prefix)}."

    @beat("{beatmsg}")
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return starts_with(self.prefix)

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
