"""
ReadsExactly an exact string.
"""

from hamcrest import has_string
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class ReadsExactly:
    """Match a specific string exactly.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_MESSAGE), ReadsExactly("Log in below."))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f'"{self.text}", verbatim.'

    @beat('... hoping it\'s "{text}", verbatim.')
    def resolve(self) -> Matcher[object]:
        """Produce the Matcher to make the assertion."""
        return has_string(self.text)

    def __init__(self, text: str) -> None:
        self.text = text
