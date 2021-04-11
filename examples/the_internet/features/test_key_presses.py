"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the Wait and Enter Actions.
"""

import unittest
from typing import Callable, Tuple

from selenium.webdriver import Firefox, Remote
from selenium.webdriver.common.by import By

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Enter, Open, See, Wait
from screenpy.pacing import act, scene
from screenpy.questions import Text
from screenpy.resolutions import ReadsExactly

from ..user_interface.key_presses import ENTRY_INPUT, RESULT_TEXT, URL


class TestKeyPresses(unittest.TestCase):
    """
    Flexes Waiting with various strategies.
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Perform")
    @scene("Wait for text")
    def test_wait_for_text(self) -> None:
        """Can select an option from a dropdown by text."""
        test_text = "H"
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(
            Enter.the_text(test_text).into_the(ENTRY_INPUT),
            Wait.for_the(RESULT_TEXT).to_contain_text(test_text),
        )
        then(Perry).should(
            See.the(Text.of_the(RESULT_TEXT), ReadsExactly(f"You entered: {test_text}"))
        )

    @act("Perform")
    @scene("Wait with custom")
    def test_wait_with_custom(self) -> None:
        """Can wait using a contrived custom wait function."""
        test_text = "H"
        Perry = self.actor

        def text_to_have_all(
            locator: Tuple[By, str], preamble: str, body: str, suffix: str
        ) -> Callable:
            """A very contrived custom condition."""

            def _predicate(driver: Remote) -> bool:
                element = driver.find_element(*locator)
                return f"{preamble} {body} {suffix}" in element.text

            return _predicate

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(
            Enter.the_text(test_text).into_the(ENTRY_INPUT),
            Wait()
            .using(text_to_have_all)
            .with_(RESULT_TEXT, "You", "entered:", test_text),
        )
        then(Perry).should(
            See.the(Text.of_the(RESULT_TEXT), ReadsExactly(f"You entered: {test_text}"))
        )

    def tearDown(self) -> None:
        self.actor.exit_stage_right()
