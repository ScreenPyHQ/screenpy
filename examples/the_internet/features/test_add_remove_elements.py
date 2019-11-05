import random
import unittest

from selenium.webdriver import Firefox

from screenpy import AnActor, given, when, then, and_
from screenpy.actions import Click, Wait
from screenpy.abilities import BrowseTheWeb
from screenpy.pacing import act, scene
from screenpy.questions import Number
from screenpy.resolutions import *

from ..tasks.start import Start
from ..user_interface.homepage import ADD_REMOVE_ELEMENTS_LINK
from ..user_interface.add_remove_elements import ADD_BUTTON, ADDED_ELEMENTS


class TestAddRemoveElements(unittest.TestCase):
    def setUp(self):
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Add And Remove")
    @scene("Add One Element")
    def test_add_one_element(self):
        Perry = self.actor

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(
            Click.on_the(ADD_REMOVE_ELEMENTS_LINK),
            Wait.for_the(ADD_BUTTON).to_appear()
        )
        and_(Perry).attempts_to(Click.on_the(ADD_BUTTON).then_wait_for(ADDED_ELEMENTS))
        then(Perry).should_see_the((Number.of(ADDED_ELEMENTS), IsEqualTo(1)))

    @act("Add And Remove")
    @scene("Add Many Elements")
    def test_add_many_elements(self):
        Perry = self.actor
        repeat = random.choice(range(2, 10))

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(
            Click.on_the(ADD_REMOVE_ELEMENTS_LINK),
            Wait.for_the(ADD_BUTTON).to_appear()
        )
        and_(Perry).attempts_to(
            *(
                Click.on_the(ADD_BUTTON).then_wait_for(ADDED_ELEMENTS)
                for each_time in range(repeat)
            )
        )
        then(Perry).should_see_the((Number.of(ADDED_ELEMENTS), IsEqualTo(repeat)))

    @act("Add And Remove")
    @scene("Remove Element")
    def test_remove_element(self):
        Perry = self.actor

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(
            Click.on_the(ADD_REMOVE_ELEMENTS_LINK),
            Wait.for_the(ADD_BUTTON).to_appear()
        )
        and_(Perry).attempts_to(Click.on_the(ADD_BUTTON).then_wait_for(ADDED_ELEMENTS))
        and_(Perry).attempts_to(Click.on_the(ADDED_ELEMENTS))
        then(Perry).should_see_the((Number.of(ADDED_ELEMENTS), IsEqualTo(0)))

    def tearDown(self):
        self.actor.exit_stage_left()
