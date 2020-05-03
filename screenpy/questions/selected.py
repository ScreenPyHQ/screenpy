"""
A question to discover the selected option or options from a dropdown or
multi-select field. Questions must be asked with an expected resolution,
like so:

    the_actor.should_see_the(
        (Selected.option_from_the(STATE_DROPDOWN), ReadsExactly("MN")),
    )
"""


from typing import List, Union

from selenium.webdriver.support.ui import Select as SeleniumSelect

from ..actor import Actor
from ..pacing import beat
from ..target import Target
from .base_question import BaseQuestion


class Selected(BaseQuestion):
    """
    Ask what options are selected in dropdowns, multi-select fields, etc.
    This question is meant to be instantiated using its static
    |Selected.option_from| or |Selected.options_from| methods. Typical
    invocations might look like:

        Selected.option_from(THE_STATE_DROPDOWN)

        Selected.options_from(INDUSTRIES)

    It can then be passed along to the |Actor| to ask the question.
    """

    target: Target
    multi: bool

    @staticmethod
    def option_from_the(target: Target) -> "Selected":
        """
        Get the option that is currently selected in a dropdown or the first
        option selected in a multi-select field.

        Note that if this method is used for a multi-select field, only the
        first selected option will be returned.

        Args:
            target: the |Target| describing the dropdown or multi-select
                element.

        Returns:
            |Selected|
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

        Args:
            multiselect_target: the |Target| describing the multi-select
                element.

        Returns:
            |Selected|
        """
        return Selected(multiselect_target, multi=True)

    options_from = options_from_the

    @beat("{0} checks the selected option(s) from {target}.")
    def answered_by(self, the_actor: Actor) -> Union[str, List[str]]:
        """
        Direct the actor to name the selected option(s).

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            str: the text of the single option selected in a dropdown, or
                the first option selected in a multi-select field.
            List[str]: the text of all options selected in a multi-select
                field.
        """
        select = SeleniumSelect(self.target.found_by(the_actor))

        if self.multi:
            return [e.text for e in select.all_selected_options]
        return select.first_selected_option.text

    def __init__(self, target: Target, multi: bool = False):
        self.target = target
        self.multi = multi
