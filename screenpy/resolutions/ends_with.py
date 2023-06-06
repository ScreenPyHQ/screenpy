"""
Matches a string which ends with a substring.
"""

from hamcrest import ends_with
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class EndsWith:
    """Match a string which ends with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_ERROR), EndsWith("username or password."))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f'Ending with "{self.postfix}".'

    @beat('... hoping it ends with "{postfix}".')
    def resolve(self) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return ends_with(self.postfix)

    def __init__(self, postfix: str) -> None:
        self.postfix = postfix
