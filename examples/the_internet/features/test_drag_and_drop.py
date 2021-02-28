"""
An example of a test module that follows the typical unittest.TestCase test
structure. These tests exercise the actions to perform drag and drop.
"""

import unittest

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Chain, HoldDown, MoveMouse, Open, Release, Wait
from screenpy.pacing import act, scene
from screenpy.questions import Text
from screenpy.resolutions import ReadsExactly

from ..user_interface.drag_and_drop import (
    FIRST_DRAGGABLE_BOX,
    SECOND_DRAGGABLE_BOX,
    URL,
)


class TestDragAndDrop(unittest.TestCase):
    """
    Shows how to do a drag-and-drop action.
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    @act("Chain")
    @scene("HoldDown")
    @scene("MoveMouse")
    @scene("Release")
    @unittest.expectedFailure
    def test_drag_and_drop(self) -> None:
        """
        User is able to drag and drop.

        Expected to fail because there is currently an issue in ActionChains.
        """
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(
            Wait.for_the(FIRST_DRAGGABLE_BOX).to_be_clickable(),
            Chain(
                HoldDown.left_mouse_button().on_the(FIRST_DRAGGABLE_BOX),
                MoveMouse.to_the(SECOND_DRAGGABLE_BOX),
                Release.left_mouse_button(),
            ),
        )
        then(Perry).should_see_the(
            (Text.of_the(FIRST_DRAGGABLE_BOX), ReadsExactly("B"))
        )

    def tearDown(self) -> None:
        self.actor.exit()
