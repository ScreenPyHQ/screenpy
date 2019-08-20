from typing import List, Union

from selenium.webdriver.support.ui import Select as SelSelect

from ..actor import Actor
from ..pacing import beat
from ..target import Target


class Selected:
    """
    Answers questions about what options are selected in dropdowns,
    multi-select fields, etc, viewed by an |Actor|. This question is meant
    to be instantiated using its static |Selected.option_from| or
    |Selected.options_from| methods. Typical invocations might look like:

        Selected.option_from(THE_STATE_DROPDOWN)
        Selected.options_from(INDUSTRIES)

    It can then be passed along to the |Actor| to ask the question.
    """

    @staticmethod
    def option_from(target: Target) -> "Selected":
        """
        Gets the option that is currently selected in a dropdown or the
        first option selected in a multiselect field.

        Args:
            target (Target): the |Target| describing the dropdown or
                multiselect element.

        Returns:
            |Selected|
        """
        return Selected(target)

    @staticmethod
    def option_from_the(target: Target) -> "Selected":
        """Syntactic sugar for |Selected.option_from|"""
        return Selected.option_from(target)

    @staticmethod
    def options_from(multiselect_target: Target) -> "Selected":
        """
        Gets all the options that are currently selected in a multiselect
        field.

        Note that this method should not be used for single-select
        dropdowns, that will cause a NotImplemented error to be raised
        from Selenium when |Selected.answered_by| is invoked.

        Args:
            multiselect_target (Target): the |Target| describing the
                multiselect element.

        Returns:
            |Selected|
        """
        return Selected(multiselect_target, multi=True)

    @staticmethod
    def options_from_the(target: Target) -> "Selected":
        """Syntactic sugar for |Selected.options_from|"""
        return Selected.options_from(target)

    @beat("{0} checks the selected option(s) from {target}")
    def answered_by(self, the_actor: Actor) -> Union[str, List[str]]:
        """
        Investigates the page as viewed by the supplied |Actor| and gives
        their answer.

        Args:
            the_actor (Actor): The |Actor| who will answer the question.

        Returns:
            str: the text of the single option selected in a dropdown, or
                the first option selected in a multiselect field.
            List[str]: the text of all options selected in a multiselect
                field.
        """
        select = SelSelect(self.target.found_by(the_actor))

        if self.multi:
            return [e.text for e in select.all_selected_options()]
        else:
            return select.first_selected_option.text

    def __init__(self, target: Target, multi: bool = False):
        self.target = target
        self.multi = multi
