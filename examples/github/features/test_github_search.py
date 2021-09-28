"""
An example of a test module that follows the typical pytest test
structure. These tests show off how to use custom tasks and Questions,
though they are a little bit contrived.
"""

from typing import Generator

import pytest
from allure_commons.types import AttachmentType

from screenpy import Actor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Open, SaveConsoleLog, SaveScreenshot, See
from screenpy.pacing import act, scene
from screenpy.resolutions import (
    ContainsTheText,
    ContainTheText,
    DoesNot,
    IsEqualTo,
    ReadsExactly,
)

from ..questions.number_of_search_results import NumberOfSearchResults
from ..questions.search_results_message import SearchResultsMessage
from ..tasks.search_github import SearchGitHub
from ..user_interface.github_home_page import URL


@pytest.fixture(scope="function", name="Perry")
def fixture_actor() -> Generator:
    """Create the Actor for our example tests!"""
    the_actor = Actor.named("Perry").who_can(BrowseTheWeb.using_chrome())
    yield the_actor
    the_actor.attempts_to(
        SaveScreenshot.as_("test.png").and_attach_it(
            name="End of Test Screenshot", attachment_type=AttachmentType.PNG
        ),
        SaveConsoleLog.as_("console_log.txt").and_attach_it(
            name="Test Console Log",
            attachment_type=AttachmentType.TEXT,
        ),
    )
    the_actor.exit_stage_left()


@act("Search")
@scene("Search for the ScreenPy repository on GitHub")
def test_search_for_screenpy(Perry: Actor) -> None:
    """GitHub search finds the screenpy repository."""
    given(Perry).was_able_to(Open.their_browser_on(URL))
    when(Perry).attempts_to(SearchGitHub.for_text("perrygoy/screenpy"))
    then(Perry).should(
        See.the(SearchResultsMessage(), DoesNot(ContainTheText("couldn’t"))),
        See.the(SearchResultsMessage(), ReadsExactly("1 repository result")),
        See.the(NumberOfSearchResults(), IsEqualTo(1)),
    )


@act("Search")
@scene("Search for a nonexistant repository on GitHub")
def test_search_for_nonexistent_repo(Perry: Actor) -> None:
    """GitHub search fails to find a nonexistant repository."""
    nonexistant_repository = "perrygoy/i-never-made-this-repo"

    given(Perry).was_able_to(Open.their_browser_on(URL))
    when(Perry).attempts_to(SearchGitHub.for_text(nonexistant_repository))
    then(Perry).should(
        See.the(SearchResultsMessage(), ContainsTheText("We couldn’t find any")),
        See.the(SearchResultsMessage(), ContainsTheText(nonexistant_repository)),
        See.the(NumberOfSearchResults(), IsEqualTo(0)),
    )
