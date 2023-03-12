"""
Matches a string which ends with a substring.
"""

from typing import TypeVar

from hamcrest import ends_with
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

SelfEndsWith = TypeVar("SelfEndsWith", bound="EndsWith")


class EndsWith:
    """Match a string which ends with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_ERROR), EndsWith("username or password."))
        )
    """

    def describe(self: SelfEndsWith) -> str:
        """Describe the Resolution in the present tense."""
        return f'Ending with {self.postfix}".'

    @beat('... hoping it\'s text ending with "{postfix}".')
    def resolve(self: SelfEndsWith) -> Matcher[str]:
        """Produce the Matcher to make the assertion."""
        return ends_with(self.postfix)

    def __init__(self, postfix: str) -> None:
        self.postfix = postfix
