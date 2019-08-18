from screenpy.questions.number import Number
from screenpy.pacing import beat

from ..user_interface.github_search_results_page import SEARCH_RESULTS


class NumberOfSearchResults:
    @beat("{0} checks the number of results...")
    def answered_by(self, the_actor):
        return Number.of(SEARCH_RESULTS).answered_by(the_actor)

    @staticmethod
    def total():
        return NumberOfSearchResults()
