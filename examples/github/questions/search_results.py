from screenpy.questions import Text
from screenpy.pacing import beat

from ..user_interface.github_search_results_page import SEARCH_RESULTS


class SearchResults:
    @staticmethod
    def list():
        return SearchResults()

    @beat("{0} checks the returned search results...")
    def answered_by(self, the_actor):
        return Text.of_all(SEARCH_RESULTS).answered_by(the_actor)

