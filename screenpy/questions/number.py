"""
A question to discover how many of an element are present on the page.
Questions must be asked with an expected resolution, like so:

    the_actor.should_see_the(
        (Number.of(RESULTS_LINKS), IsNot(EqualTo(0))),
    )
"""


from ..actor import Actor
from ..pacing import beat
from ..target import Target


class Number:
    """
    Ask how many of a certain element are on the page, viewed by an
    |Actor|. This question is meant to be instantiated via its static
    |Number.of| method. A typical invocation might look like:

        Number.of(SEARCH_RESULTS)

    It can then be passed along to the |Actor| to ask the question.
    """

    target: Target

    @staticmethod
    def of(target: Target) -> "Number":
        """
        Specify the target to count.

        Args:
            target: the |Target| describing the element to count.

        Returns:
            |Number|
        """
        return Number(target=target)

    @beat("{} counts the number of {target}.")
    def answered_by(self, the_actor: Actor) -> int:
        """
        Direct the actor to count the elements.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            int
        """
        return len(self.target.all_found_by(the_actor))

    def __init__(self, target: Target) -> None:
        self.target = target
