"""
A question to discover the text of an element or many elements. Questions
must be asked with an expected resolution, like so:

    the_actor.should_see_the(
        (Text.of_the(WELCOME_BANNER), ReadsExactly("Welcome!")),
    )
"""


from typing import List, Union

from ..actor import Actor
from ..pacing import beat
from ..target import Target


class Text:
    """
    Ask what text appears in an element or elements, viewed by an |Actor|.
    This question is meant to be instantiated using its static |Text.of| or
    |Text.of_all| methods. Typical invocations might look like:

        Text.of(THE_WELCOME_HEADER)

        Text.of_all(SEARCH_RESULTS)

    It can then be passed along to the |Actor| to ask the question.
    """

    target: Target
    multi: bool

    @staticmethod
    def of_the(target: Target) -> "Text":
        """
        Specify the target to read, expecting this target to describe a single
        element or the first of many elements (e.g. "#loginlink").

        Args:
            target: the |Target| describing the element to read.

        Returns:
            |Text|
        """
        return Text(target=target)

    of = of_the

    @staticmethod
    def of_all(multi_target: Target) -> "Text":
        """
        Specify the target to read, expecting this target to describe multiple
        elements.

        Args:
            multi_target: the |Target| describing the elements to read.

        Returns:
            |Text|
        """
        return Text(target=multi_target, multi=True)

    @beat("{} reads the text from the {target}.")
    def answered_by(self, the_actor: Actor) -> Union[str, List[str]]:
        """
        Direct the actor to read off the targeted element's text.

        Args:
            the_actor: the |Actor| who will answer the question.

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
