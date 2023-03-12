"""
Matches a list that contains the desired item.
"""

from typing import Sequence, TypeVar

from hamcrest import has_item
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat

SelfContainsTheItem = TypeVar("SelfContainsTheItem", bound="ContainsTheItem")
T = TypeVar("T")


class ContainsTheItem:
    """Match an iterable containing a specific item.

    Examples::

        the_actor.should(
            See.the(Text.of_all(SEARCH_RESULTS), ContainsTheItem("The Droids"))
        )
    """

    def describe(self: SelfContainsTheItem) -> str:
        """Describe the Resolution in present tense."""
        return f'Match a list containing "{self.item}".'

    @beat('... hoping it\'s a list containing the item "{item}".')
    def resolve(self: SelfContainsTheItem) -> Matcher[Sequence[T]]:
        """Produce the Matcher to make the assertion."""
        return has_item(self.item)

    def __init__(self: SelfContainsTheItem, item: T) -> None:
        self.item = item
