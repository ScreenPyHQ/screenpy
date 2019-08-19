from typing import List, Union

from ..actor import Actor
from ..pacing import beat
from ..target import Target


class Text(object):
    """
    Asks what text appears in an element or elements, viewed by an
    |Actor|. This question is meant to be instantiated using its static
    |Text.of| or |Text.of_all| methods. Typical invocations might look
    like:

        Text.of(THE_WELCOME_HEADER)
        Text.of_all(SEARCH_RESULTS)

    It can then be passed along to the |Actor| to ask the question.
    """

    @staticmethod
    def of(target: Target) -> "Text":
        """
        Provides the target to read.

        Args:
            target (Target): the |Target| describing the element to read.

        Returns:
            |Text|
        """
        return Text(target=target)

    @staticmethod
    def of_all(multi_target: Target) -> "Text":
        """
        Provides the targets to read.

        Args:
            multi_target (Target): the |Target| describing the elements to
                read.

        Returns:
            |Text|
        """
        return Text(target=multi_target, multi=True)

    @beat("{} reads the text from {target}")
    def answered_by(self, the_actor: Actor) -> Union[str, List[str]]:
        """
        Investigates the page as viewed by the supplied |Actor| and gives
        their answer.

        Args:
            the_actor (Actor): The |Actor| who will answer the question.

        Returns:
            str: the text of the single element found by target.
            List[str]: the text of all elements found by target.
        """
        if self.multi:
            return [e.text for e in self.target.all_found_by(the_actor)]
        return self.target.found_by(the_actor).text

    def __init__(self, target: Target, multi: bool = False) -> None:
        self.target = target
        self.multi = multi
