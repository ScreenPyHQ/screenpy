"""
Matches a substring.
"""

from hamcrest import contains_string
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class ContainsTheText:
    """Match a specific substring of a string.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), ContainsTheText("Hello,"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f'Containing the text "{self.text}".'

    @beat('... hoping it contains "{text}".')
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return contains_string(self.text)

    def __init__(self, text: str) -> None:
        self.text = text
