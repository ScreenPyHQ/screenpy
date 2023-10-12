"""Matches a substring in a string."""

from hamcrest import contains_string
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop


class ContainsTheText:
    """Match a specific substring of a string.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), ContainsTheText("Hello,"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Containing the text {self.text_to_log}."

    @beat("... hoping it contains {text_to_log}.")
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return contains_string(self.text)

    def __init__(self, text: str) -> None:
        self.text = text
        self.text_to_log = represent_prop(text)
