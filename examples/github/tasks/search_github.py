from selenium.webdriver.common.keys import Keys

from screenpy.actions.enter import Enter
from screenpy.pacing import beat, NORMAL

from ..user_interface.github_header_bar import SEARCH_INPUT
from ..user_interface.github_search_results_page import RESULTS_MESSAGE


class SearchGitHub(object):
    @beat("{0} searches GitHub for '{search_query}'", severity=NORMAL)
    def perform_as(self, the_actor):
        the_actor.attempts_to(
            Enter.the_text(self.search_query)
            .into(SEARCH_INPUT)
            .then_hit(Keys.RETURN)
            .then_wait_for(RESULTS_MESSAGE)
        )

    @staticmethod
    def for_text(search_query):
        return SearchGitHub(search_query)

    def __init__(self, search_query):
        self.search_query = search_query
