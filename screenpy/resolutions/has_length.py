"""Matches the length of a collection."""

from typing import Sized

from hamcrest import has_length
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat


class HasLength:
    """Match against a collection with a specific length.

    Examples::

        the_actor.should(
            See.the(Selected.options_from(INDUSTRIES), HasLength(5))
        )
    """

    @property
    def item_plural(self) -> str:
        """Decide if we need "item" or "items" in the beat message."""
        return "items" if self.length != 1 else "item"

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"{self.length} {self.item_plural} long."

    @beat("... hoping it's a collection with {length} {item_plural} in it.")
    def resolve(self) -> Matcher[Sized]:
        """Produce the Matcher to make the assertion."""
        return has_length(self.length)

    def __init__(self, length: int) -> None:
        self.length = length
