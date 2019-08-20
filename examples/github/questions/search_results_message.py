from screenpy.questions import Text
from screenpy.pacing import beat

from ..user_interface.github_search_results_page import RESULTS_MESSAGE


class SearchResultsMessage:
    @staticmethod
    def text():
        return SearchResultsMessage()

    @beat("{0} checks the results message...")
    def answered_by(self, the_actor):
        return Text.of(RESULTS_MESSAGE).answered_by(the_actor)
