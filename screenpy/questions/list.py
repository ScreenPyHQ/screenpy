"""
Investigate one or more elements.
"""

from typing import List as ListType

from selenium.webdriver.remote.webdriver import WebElement

from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target


class List:
    """Ask for a list of elements.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should(See.the(List.of(CONFETTI), IsEmpty()))
    """

    @staticmethod
    def of_the(target: Target) -> "List":
        """Target the element(s) to list."""
        return List(target)

    of_all_the = of_all = of = of_the

    def describe(self) -> str:
        """Describe the Question.."""
        return f"The list of {self.target}."

    @beat("{} lists off the {target}.")
    def answered_by(self, the_actor: Actor) -> ListType[WebElement]:
        """Direct the Actor to rattle off the specified elements."""
        return self.target.all_found_by(the_actor)

    def __init__(self, target: Target) -> None:
        self.target = target
