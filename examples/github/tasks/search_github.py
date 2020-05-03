"""
A slightly more interesting task to search GitHub for a string.
"""


from screenpy import Actor
from screenpy.actions import Enter, Wait
from screenpy.pacing import beat
from selenium.webdriver.common.keys import Keys

from ..user_interface.github_header_bar import SEARCH_INPUT
from ..user_interface.github_search_results_page import RESULTS_MESSAGE


class SearchGitHub:
    """
    A task to search GitHub for a specific query. Give this task to your
    actors like so:

        the_actor.attempts_to(SearchGitHub.for_text("screenpy"))
    """

    @staticmethod
    def for_text(search_query: str) -> "SearchGitHub":
        """
        Supply the text to search GitHub for.

        Args:
            search_query: the text to enter into the search bar.
        """
        return SearchGitHub(search_query)

    @beat("{0} searches GitHub for '{search_query}'")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to search github for the given term.

        Args:
            the_actor: the actor who will perform this task.
        """
        the_actor.attempts_to(
            Enter.the_text(self.search_query).into(SEARCH_INPUT).then_hit(Keys.RETURN),
            Wait.for_the(RESULTS_MESSAGE),
        )

    def __init__(self, search_query):
        self.search_query = search_query
