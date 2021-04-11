"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the alert checking Actions.
"""

import unittest

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import (
    AcceptAlert,
    Click,
    DismissAlert,
    Open,
    RespondToPrompt,
    See,
)
from screenpy.pacing import act, scene
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
    Flexes the AcceptAlert, DismissAlert, and RespondToPrompt Actions, as
    well as the TextOfTheAlert Question.
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    @act("Perform")
    @scene("TextOfTheAlert")
    def test_inspect_alert(self) -> None:
        """User can read the text of the alert."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Click.on_the(JS_ALERT_BUTTON))
        then(Perry).should(See.the(TextOfTheAlert(), ReadsExactly("I am a JS Alert")))

    @act("Perform")
    @scene("AcceptAlert")
    def test_accept_alert(self) -> None:
        """User can accept an alert."""
        Perry = self.actor

        given(Perry).was_able_to(
            Open.their_browser_on(URL), Click.on_the(JS_CONFIRM_BUTTON)
        )
        when(Perry).attempts_to(AcceptAlert())
        then(Perry).should(
            See.the(Text.of_the(RESULT_MESSAGE), ReadsExactly("You clicked: Ok"))
        )

    @act("Perform")
    @scene("DismissAlert")
    def test_dismiss_alert(self) -> None:
        """User can dismiss an alert."""
        Perry = self.actor

        given(Perry).was_able_to(
            Open.their_browser_on(URL), Click.on_the(JS_CONFIRM_BUTTON)
        )
        when(Perry).attempts_to(DismissAlert())
        then(Perry).should(
            See.the(Text.of_the(RESULT_MESSAGE), ReadsExactly("You clicked: Cancel"))
        )

    @act("Perform")
    @scene("RespondToPrompt")
    def test_respond_to_prompt(self) -> None:
        """User can enter text into a prompt."""
        Perry = self.actor
        test_text = "Hello! I am responding to this prompt."

        given(Perry).was_able_to(
            Open.their_browser_on(URL), Click.on_the(JS_PROMPT_BUTTON)
        )
        when(Perry).attempts_to(RespondToPrompt.with_(test_text))
        then(Perry).should(
            See.the(
                Text.of_the(RESULT_MESSAGE), ReadsExactly(f"You entered: {test_text}")
            )
        )

    def tearDown(self) -> None:
        self.actor.exit()
