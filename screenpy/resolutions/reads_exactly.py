"""Matches an exact string."""

from hamcrest import has_string
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop


class ReadsExactly:
    """Match a specific string exactly.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_MESSAGE), ReadsExactly("Log in below."))
        )
    """

    @property
    def text_to_log(self) -> str:
        """Represent the text in a log-friendly way."""
        return represent_prop(self.text)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"{self.text_to_log}, verbatim."

    @beat("... hoping it's {text_to_log}, verbatim.")
    def resolve(self) -> Matcher[object]:
        """Produce the Matcher to make the assertion."""
        return has_string(self.text)

    def __init__(self, text: str) -> None:
        self.text = text
