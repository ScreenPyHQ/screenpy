"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the clicking and waiting Actions.
"""

import random
import unittest

from selenium.webdriver import Firefox

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Click, Open, See, Wait
from screenpy.pacing import act, scene
from screenpy.questions import Element, Number
from screenpy.resolutions import IsEqualTo, IsVisible

from ..user_interface.add_remove_elements import ADD_BUTTON, ADDED_ELEMENTS, URL


class TestAddRemoveElements(unittest.TestCase):
    """
    Flexes the Add and Remove Elements page of http://the-internet.herokuapp.com/
    """

    def setUp(self) -> None:
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Perform")
    @scene("Click")
    def test_add_one_element(self) -> None:
        """User is able to add one element."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Click.on_the(ADD_BUTTON), Wait.for_the(ADDED_ELEMENTS))
        then(Perry).should(See.the(Element(ADDED_ELEMENTS), IsVisible()))

    @act("Perform")
    @scene("Click")
    def test_add_many_elements(self) -> None:
        """
        User is able to add many elements. This test chooses a random
        number of elements to add, just to show off how to do that, if you
        want to do something like that.
        """
        Perry = self.actor
        number_of_times = random.choice(range(2, 10))

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(
            *(Click.on_the(ADD_BUTTON) for each_time in range(number_of_times))
        )
        then(Perry).should(
            See.the(Number.of(ADDED_ELEMENTS), IsEqualTo(number_of_times))
        )

    @act("Perform")
    @scene("Click")
    def test_remove_element(self) -> None:
        """User is able to remove an element that was added."""
        Perry = self.actor

        given(Perry).was_able_to(
            Open.their_browser_on(URL),
            Click.on_the(ADD_BUTTON),
            Wait.for_the(ADDED_ELEMENTS),
        )
        when(Perry).attempts_to(Click.on_the(ADDED_ELEMENTS))
        then(Perry).should(See.the(Number.of(ADDED_ELEMENTS), IsEqualTo(0)))

    def tearDown(self) -> None:
        self.actor.exit_stage_left()
