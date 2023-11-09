"""Matches a list that contains the desired item."""

from typing import Generic, Sequence, TypeVar

from hamcrest import has_item
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

T = TypeVar("T")


class ContainsTheItem(Generic[T]):
    """Match an iterable containing a specific item.

    Examples::

        the_actor.should(
            See.the(Text.of_all(SEARCH_RESULTS), ContainsTheItem("The Droids"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"A sequence containing {self.item_to_log}."

    @beat("... hoping it contains {item_to_log}.")
    def resolve(self) -> Matcher[Sequence[T]]:
        """Produce the Matcher to make the assertion."""
        return has_item(self.item)

    def __init__(self, item: T) -> None:
        self.item = item
        self.item_to_log = represent_prop(item)
