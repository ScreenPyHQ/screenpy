"""
Investigate how many of an element are present on the page.
"""

from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target


class Number:
    """Ask how many of a certain element are on the page.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should(See.the(Number.of(SEARCH_RESULTS), IsEqualTo(4)))
    """

    @staticmethod
    def of(target: Target) -> "Number":
        """Target the element to be counted."""
        return Number(target=target)

    def describe(self) -> str:
        """Describe the Question.."""
        return f"The number of {self.target}."

    @beat("{} counts the number of {target}.")
    def answered_by(self, the_actor: Actor) -> int:
        """Direct the Actor to count the elements."""
        return len(self.target.all_found_by(the_actor))

    def __init__(self, target: Target) -> None:
        self.target = target
