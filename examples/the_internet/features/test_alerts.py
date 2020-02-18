"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the alert checking actions.
"""


import unittest

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import AcceptAlert, Click, DismissAlert, Open, RespondToPrompt
from screenpy.questions import Text, TextOfTheAlert
from screenpy.resolutions import ReadsExactly

from ..user_interface.javascript_alerts import (
    JS_ALERT_BUTTON,
    JS_CONFIRM_BUTTON,
    JS_PROMPT_BUTTON,
    RESULT_MESSAGE,
    URL,
)


class TestAlerts(unittest.TestCase):
    """
    Flexes the AcceptAlert, DismissAlert, and RespondToPrompt actions, as
    well as the TextOfTheAlert question.
    """

    def setUp(self):
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    def test_inspect_alert(self):
        """User can read the text of the alert."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Click.on_the(JS_ALERT_BUTTON))
        then(Perry).should_see_the((TextOfTheAlert(), ReadsExactly("I am a JS Alert")))

    def test_accept_alert(self):
        """User can accept an alert."""
        Perry = self.actor

        given(Perry).was_able_to(
            Open.their_browser_on(URL), Click.on_the(JS_CONFIRM_BUTTON)
        )
        when(Perry).attempts_to(AcceptAlert())
        then(Perry).should_see_the(
            (Text.of_the(RESULT_MESSAGE), ReadsExactly("You clicked: Ok"))
        )

    def test_dismiss_alert(self):
        """User can dismiss an alert."""
        Perry = self.actor

        given(Perry).was_able_to(
            Open.their_browser_on(URL), Click.on_the(JS_CONFIRM_BUTTON)
        )
        when(Perry).attempts_to(DismissAlert())
        then(Perry).should_see_the(
            (Text.of_the(RESULT_MESSAGE), ReadsExactly("You clicked: Cancel"))
        )

    def test_respond_to_prompt(self):
        """User can enter text into a prompt."""
        Perry = self.actor
        test_text = "Hello! I am responding to this prompt."

        given(Perry).was_able_to(
            Open.their_browser_on(URL), Click.on_the(JS_PROMPT_BUTTON)
        )
        when(Perry).attempts_to(RespondToPrompt.with_(test_text))
        then(Perry).should_see_the(
            (Text.of_the(RESULT_MESSAGE), ReadsExactly(f"You entered: {test_text}"))
        )

    def tearDown(self):
        self.actor.exit()
