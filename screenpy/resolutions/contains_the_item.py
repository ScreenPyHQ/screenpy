"""
Matches a list that contains the desired item.
"""

from typing import Sequence, TypeVar

from hamcrest import has_item
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

T = TypeVar("T")


class ContainsTheItem:
    """Match an iterable containing a specific item.

    Examples::

        the_actor.should(
            See.the(Text.of_all(SEARCH_RESULTS), ContainsTheItem("The Droids"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f'A sequence containing "{self.item}".'

    @beat('... hoping it contains "{item}".')
    def resolve(self) -> Matcher[Sequence[T]]:
        """Produce the Matcher to make the assertion."""
        return has_item(self.item)

    def __init__(self, item: T) -> None:
        self.item = item
