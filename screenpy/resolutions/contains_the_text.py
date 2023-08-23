"""
Matches a substring.
"""

from hamcrest import contains_string
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import tostring


class ContainsTheText:
    """Match a specific substring of a string.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), ContainsTheText("Hello,"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Containing the text {tostring(self.text)}."

    @property
    def beatmsg(self) -> str:
        """format string meant for beat msg"""
        return f"... hoping it contains {tostring(self.text)}."

    @beat("{beatmsg}")
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return contains_string(self.text)

    def __init__(self, text: str) -> None:
        self.text = text
