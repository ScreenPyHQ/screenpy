"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the SwitchToTab Action.
"""

import unittest

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Click, Open, Pause, See, SwitchToTab
from screenpy.pacing import act, scene
from screenpy.questions import BrowserURL, Text
from screenpy.resolutions import ContainsTheText, ReadsExactly

from ..user_interface.multiple_windows import CLICK_HERE_LINK, HEADER_MESSAGE, URL


class TestTabs(unittest.TestCase):
    """
    Flexes the SwitchToTab Action.
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    @act("Perform")
    @scene("SwitchToTab")
    def test_switch_to_new_tab(self) -> None:
        """User is able to switch to a new tab."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(
            Click.on_the(CLICK_HERE_LINK),
            Pause.for_(1).second_because("Selenium needs to catch up"),
            SwitchToTab(2),
        )
        then(Perry).should(
            See.the(BrowserURL(), ContainsTheText("windows/new")),
            See.the(Text.of_the(HEADER_MESSAGE), ReadsExactly("New Window")),
        )

    def tearDown(self) -> None:
        self.actor.exit()
