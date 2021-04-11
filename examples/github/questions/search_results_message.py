"""
A Question for finding out the displayed search results message.
"""


from screenpy import Actor
from screenpy.pacing import beat
from screenpy.questions import Text

from ..user_interface.github_search_results_page import RESULTS_MESSAGE


class SearchResultsMessage:
    """Find the text of the search results message.

    Abilities Required:
        BrowseTheWeb

    Examples::

        the_actor.should(
            See.the(SearchResultsMessage(), ReadsExactly("1 repository result")),
        )
    """

    @beat("{} checks the results message...")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to read off the text of the results message."""
        return Text.of(RESULTS_MESSAGE).answered_by(the_actor)
