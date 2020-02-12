"""
An example of a test module that follows the typical unittest.TestCase
test structure.
"""


import unittest

from screenpy import AnActor, and_, given, then, when
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Click, Select
from screenpy.pacing import act, scene
from screenpy.questions import Selected
from screenpy.resolutions import ReadsExactly
from selenium.webdriver import Firefox

from ..tasks.start import Start
from ..user_interface.dropdown import THE_DROPDOWN
from ..user_interface.homepage import DROPDOWN_LINK


class TestDropdowns(unittest.TestCase):
    """
    Uses each selection strategy to select an option from a dropdown.
    """

    def setUp(self):
        self.actor = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    @act("Select")
    @scene("Select by text")
    def test_select_by_text(self):
        """Can select an option from a dropdown by text."""
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
        """Can select an option from a dropdown by index."""
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
        """Can select an option from a dropdown by value."""
        Perry = self.actor

        given(Perry).was_able_to(Start.on_the_homepage())
        when(Perry).attempts_to(Click.on_the(DROPDOWN_LINK).then_wait_for(THE_DROPDOWN))
        and_(Perry).attempts_to(Select.the_option_with_value(2).from_(THE_DROPDOWN))
        then(Perry).should_see_the(
            (Selected.option_from(THE_DROPDOWN), ReadsExactly("Option 2"))
        )

    def tearDown(self):
        self.actor.exit_stage_right()
