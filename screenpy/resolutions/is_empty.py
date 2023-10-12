"""Matches an empty collection."""

from typing import Sized

from hamcrest import empty
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class IsEmpty:
    """Match on an empty collection.

    Examples::

        the_actor.should(See.the(List.of_all(VIDEO_FRAMES), IsEmpty()))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "An empty collection."

    @beat("... hoping it's an empty collection.")
    def resolve(self) -> Matcher[Sized]:
        """Produce the Matcher to make the assertion."""
        return empty()
