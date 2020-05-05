"""
A question to retrieve the element from the page, for further validation.
Questions must be asked with an expected resolution, like so:

    the_actor.should_see_the((Element(WELCOME_BANNER), IsVisible()))
"""


from selenium.webdriver.remote.webelement import WebElement

from ..actor import Actor
from ..pacing import beat
from ..target import Target
from .base_question import BaseQuestion


class Element(BaseQuestion):
    """
    Ask to retrieve a specific element. This question is meant to be
    instantiated with a target. A typical invocation might look like:

        Element(WELCOME_BANNER)

    It can then be passed along to the |Actor| to ask the question.
    """

    @beat("{} views the '{target}' element.")
    def answered_by(self, the_actor: Actor) -> WebElement:
        """
        Direct the actor to find the element.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            |WebElement|
        """
        return self.target.found_by(the_actor)

    def __init__(self, target: Target) -> None:
        self.target = target
