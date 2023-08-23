"""
Matches a string which ends with a substring.
"""

from hamcrest import ends_with
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import tostring


class EndsWith:
    """Match a string which ends with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_ERROR), EndsWith("username or password."))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Ending with {tostring(self.postfix)}."

    @property
    def beatmsg(self) -> str:
        """format string meant for beat msg"""
        return f"... hoping it ends with {tostring(self.postfix)}."

    @beat("{beatmsg}")
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return ends_with(self.postfix)

    def __init__(self, postfix: str) -> None:
        self.postfix = postfix
