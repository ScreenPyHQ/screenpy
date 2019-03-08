from screenpy.questions.text import Text
from screenpy.pacing import beat

from ..user_interface.github_search_results_page import SEARCH_RESULTS


class SearchResults(object):
    @beat("{0} checks the returned search results...")
    def answered_by(self, the_actor):
        return Text.of_all(SEARCH_RESULTS).viewed_by(the_actor)

    @staticmethod
    def list():
        return SearchResults()
