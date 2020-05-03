"""
A question for finding out the displayed search results message. It is a
little contrived, but it shows how to write your own question.
"""


from screenpy import Actor
from screenpy.pacing import beat
from screenpy.questions import Text

from ..user_interface.github_search_results_page import RESULTS_MESSAGE


class SearchResultsMessage:
    """
    Find the text of the search results message. Pass it to an actor like
    so:

        the_actor.should_see_the(
            (SearchResultsMessage(), ReadsExactly("1 repository result"))
        )
    """

    @beat("{0} checks the results message...")
    def answered_by(self, the_actor: Actor) -> str:
        """
        Direct the actor to read off the text of the results message.

        Args:
            the_actor:
        """
        return Text.of(RESULTS_MESSAGE).answered_by(the_actor)
