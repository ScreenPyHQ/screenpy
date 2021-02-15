"""
A question to discover the text of the selected option or options from a
dropdown or multi-select field.
"""

from typing import List, Union

from selenium.webdriver.support.ui import Select as SeleniumSelect

from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target


class Selected:
    """Ask for the text of selected option(s) in a dropdown or multi-select field.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should_see_the(
            (Selected.option_from(THE_STATE_DROPDOWN), ReadsExactly("Minnesota")),
        )

        the_actor.should_see_the((Selected.options_from(INDUSTRIES), HasLength(5)))
    """

    @staticmethod
    def option_from_the(target: Target) -> "Selected":
        """
        Get the option that is currently selected in a dropdown or the first
        option selected in a multi-select field.

        Note that if this method is used for a multi-select field, only the
        first selected option will be returned.
        """
        return Selected(target)

    option_from = option_from_the

    @staticmethod
    def options_from_the(multiselect_target: Target) -> "Selected":
        """
        Get all the options that are currently selected in a multi-select
        field.

        Note that this method should not be used for single-select dropdowns,
        that will cause a NotImplemented error to be raised from Selenium when
        answering this question.
        """
        return Selected(multiselect_target, multi=True)

    options_from = options_from_the

    @beat("{} checks the selected option(s) from {target}.")
    def answered_by(self, the_actor: Actor) -> Union[str, List[str]]:
        """Direct the actor to name the selected option(s)."""
        select = SeleniumSelect(self.target.found_by(the_actor))

        if self.multi:
            return [e.text for e in select.all_selected_options]
        return select.first_selected_option.text

    def __init__(self, target: Target, multi: bool = False):
        self.target = target
        self.multi = multi
