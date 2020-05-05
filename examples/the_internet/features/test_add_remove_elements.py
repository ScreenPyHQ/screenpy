"""
An example of a test module that follows the typical unittest.TestCase
test structure. These tests exercise the clicking and waiting actions.
"""


import random
import unittest

from screenpy import AnActor, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Click, Open, Wait
from screenpy.pacing import act, scene
from screenpy.questions import Element, Number
from screenpy.resolutions import IsEqualTo, IsVisible
from selenium.webdriver import Firefox

from ..user_interface.add_remove_elements import ADD_BUTTON, ADDED_ELEMENTS, URL


class TestAddRemoveElements(unittest.TestCase):
    """
    Flexes the Add and Remove Elements page of http://the-internet.herokuapp.com/
    """

    def setUp(self):
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Perform")
    @scene("Click")
    def test_add_one_element(self):
        """User is able to add one element."""
        Perry = self.actor

        given(Perry).was_able_to(Open.their_browser_on(URL))
        when(Perry).attempts_to(Click.on_the(ADD_BUTTON), Wait.for_the(ADDED_ELEMENTS))
        then(Perry).should_see_the((Element(ADDED_ELEMENTS), IsVisible()))

    @act("Perform")
    @scene("Click")
    def test_add_many_elements(self):
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
        then(Perry).should_see_the(
            (Number.of(ADDED_ELEMENTS), IsEqualTo(number_of_times))
        )

    @act("Perform")
    @scene("Click")
    def test_remove_element(self):
        """User is able to remove an element that was added."""
        Perry = self.actor

        given(Perry).was_able_to(
            Open.their_browser_on(URL),
            Click.on_the(ADD_BUTTON),
            Wait.for_the(ADDED_ELEMENTS),
        )
        when(Perry).attempts_to(Click.on_the(ADDED_ELEMENTS))
        then(Perry).should_see_the((Number.of(ADDED_ELEMENTS), IsEqualTo(0)))

    def tearDown(self):
        self.actor.exit_stage_left()
