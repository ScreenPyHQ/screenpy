"""Matches a string which begins with a substring."""

from hamcrest import starts_with
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop


class StartsWith:
    """Match a string which starts with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), StartsWith("Welcome"))
        )
    """

    @property
    def prefix_to_log(self) -> str:
        """Represent the prefix in a log-friendly way."""
        return represent_prop(self.prefix)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Starting with {self.prefix_to_log}."

    @beat("... hoping it starts with {prefix_to_log}.")
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return starts_with(self.prefix)

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
