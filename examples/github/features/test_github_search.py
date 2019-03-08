import unittest

from selenium.webdriver import Firefox

from screenpy.actors.actor import Actor
from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.pacing import act, scene
from screenpy.given_when_then import *
from screenpy.resolutions import *

from ..questions.search_results_message import SearchResultsMessage
from ..questions.number_of_search_results import NumberOfSearchResults
from ..tasks.start import Start
from ..tasks.search_github import SearchGitHub


class TestGitHubSearch(unittest.TestCase):
    def setUp(self):
        self.perry = Actor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Search")
    @scene("Search for the ScreenPy repository on GitHub")
    def test_search_for_screenpy(self):
        perry = self.perry

        given(perry).was_able_to(Start.on_the_homepage())
        when(perry).attempts_to(SearchGitHub.for_text("perrygoy/screenpy"))
        then(perry).should_see_that(
            (SearchResultsMessage.text(), DoesNot(ContainTheText("couldn’t"))),
            (SearchResultsMessage.text(), ReadsExactly("1 repository result")),
            (NumberOfSearchResults.total(), IsEqualTo(1)),
        )

    @act("Search")
    @scene("Search for a nonexistant repository on GitHub")
    def test_search_for_nonexistent_repo(self):
        nonexistant_repository = "perrygoy/i-never-made-this-repo"
        perry = self.perry

        given(perry).was_able_to(Start.on_the_homepage())
        when(perry).attempts_to(SearchGitHub.for_text(nonexistant_repository))
        then(perry).should_see_that(
            (SearchResultsMessage.text(), ContainsTheText("We couldn’t find any")),
            (SearchResultsMessage.text(), ContainsTheText(nonexistant_repository)),
            (NumberOfSearchResults.total(), IsEqualTo(0)),
        )

    def tearDown(self):
        self.perry.exit_stage_left()
