"""
A question to discover the text of an element or many elements. Questions
must be asked with an expected resolution, like so:

    the_actor.should_see_the(
        (Text.of_the(WELCOME_BANNER), ReadsExactly("Welcome!")),
    )
"""


from typing import List as ListType

from selenium.webdriver.remote.webdriver import WebElement

from ..actor import Actor
from ..pacing import beat
from ..target import Target
from .base_question import BaseQuestion


class List(BaseQuestion):
    """
    Ask for a list of elements, viewed by an |Actor|. This question is
    meant to be instantiated using its static |List.of| or |List.of_all|
    methods. Typical invocations might look like:

        List.of(SEARCH_RESULTS)

        List.of_all(IMAGES)

    It can then be passed along to the |Actor| to ask the question.
    """

    target: Target

    @staticmethod
    def of_the(target: Target) -> "List":
        """
        Specify the target to list.

        Args:
            target: the |Target| describing the elements to list out.

        Returns:
            |List|
        """
        return List(target)

    of_all_the = of_all = of = of_the

    @beat("{} lists off the {target}.")
    def answered_by(self, the_actor: Actor) -> ListType[WebElement]:
        """
        Direct the actor to rattle off the specified elements.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            List[|WebElement|]
        """
        return self.target.all_found_by(the_actor)

    def __init__(self, target: Target) -> None:
        self.target = target
