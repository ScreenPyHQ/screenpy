import unittest

from selenium.webdriver import Firefox

from screenpy.actors.actor import AnActor
from screenpy.actions.click import Click
from screenpy.actions.select import Select
from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.given_when_then import *
from screenpy.pacing import act, scene
from screenpy.questions.selected import Selected
from screenpy.resolutions import *

from ..tasks.start import Start
from ..user_interface.homepage import DROPDOWN_LINK
from ..user_interface.dropdown import THE_DROPDOWN


class TestDropdowns(unittest.TestCase):
    def setUp(self):
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Select")
    @scene("Select by text")
    def test_select_by_text(self):
        Perry = self.actor

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(Click.on_the(DROPDOWN_LINK).then_wait_for(THE_DROPDOWN))
        and_(Perry).attempts_to(Select.the_option_named("Option 1").from_(THE_DROPDOWN))
        then(Perry).should_see_the(
            (Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Select")
    @scene("Select by index")
    def test_select_by_index(self):
        Perry = self.actor

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(Click.on_the(DROPDOWN_LINK).then_wait_for(THE_DROPDOWN))
        and_(Perry).attempts_to(Select.the_option_at_index(1).from_(THE_DROPDOWN))
        then(Perry).should_see_the(
            (Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 1"))
        )

    @act("Select")
    @scene("Select by value")
    def test_select_by_value(self):
        Perry = self.actor

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(Click.on_the(DROPDOWN_LINK).then_wait_for(THE_DROPDOWN))
        and_(Perry).attempts_to(Select.the_option_with_value(2).from_(THE_DROPDOWN))
        then(Perry).should_see_the(
            (Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 2"))
        )

    def tearDown(self):
        self.actor.exit_stage_right()
