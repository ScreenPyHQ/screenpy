"""
A question to find out the number of search results on the GitHub search
page. It is a little contrived, but it shows how to write your own
question.
"""

from screenpy import Actor
from screenpy.pacing import beat
from screenpy.questions import Number

from ..user_interface.github_search_results_page import SEARCH_RESULTS


class NumberOfSearchResults:
    """
    Find the number of search results. Pass it to an actor like so:

        the_actor.should_see_the((NumberOfSearchResults(), Equals(4)))
    """

    @beat("{0} checks the number of results...")
    def answered_by(self, the_actor: Actor) -> float:
        """
        Direct the actor to count the number of search results.

        Args:
            the_actor: the actor who will answer the question.

        Returns:
            float
        """
        return Number.of(SEARCH_RESULTS).answered_by(the_actor)
