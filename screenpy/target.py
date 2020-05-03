"""
Provides an object to store a locator with a human-readable string. The
human-readable string will be used in logging and reporting; the locator
will be used by actors to find elements.
"""


from typing import List, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from .abilities.browse_the_web import BrowseTheWeb
from .actor import Actor
from .exceptions import TargetingError


class Target:
    """
    A class to contain information about an element. This class stores a
    nice human-readable string describing an element along with either an
    XPath or a CSS selector string. It is intended to be instantiated by
    calling its static |Target.the| method. A typical invocation might
    look like:

        Target.the("header search bar").located_by("div.searchbar")

    It can then be used in Questions, Actions or Tasks to access that
    element.
    """

    target_name: str
    locator: Union[None, Tuple[By, str]]

    @staticmethod
    def the(desc: str) -> "Target":
        """
        Provide a human-readable description. This method call should be
        followed up with a call to |Target.located_by|.

        Args:
            desc (str): The human-readable description for the targeted
                element. Beginning with a lower-case letter makes the
                allure test logs look the nicest.

        Returns:
            |Target|
        """
        return Target(desc)

    def located(self, locator: Tuple[By, str]) -> "Target":
        """
        Supply an instantiated target with a locator. This locator is a
        tuple of the By strategy to use and the identifying string, e.g.

            Target.the("signout link").located((By.LINK_TEXT, "Sign Out"))

        Args:
            locator: the (|By|, str) tuple to use to find the element.

        Returns:
            |Target|
        """
        self.locator = locator
        return self

    def located_by(self, locator: str) -> "Target":
        """
        Supply an instantiated Target with a locator string, which is either a
        CSS selector or an XPATH string.

        Args:
            locator: the string to use as a locator for the element.
                Can be a CSS selector or an xpath string.

        Returns:
            |Target|
        """
        if locator.startswith("/"):
            self.locator = (By.XPATH, locator)
        else:
            self.locator = (By.CSS_SELECTOR, locator)

        return self

    def get_locator(self) -> Tuple[By, str]:
        """
        Return the stored locator as a (By, str) tuple.

        Returns:
            Tuple(|By|, str)

        Raises:
            |TargetingError|: if no locator was supplied to the target.
        """
        if self.locator is None:
            raise TargetingError(
                f"Locator was not supplied to the {self} target. Make sure to use "
                "either .located() or .located_by() to supply a locator."
            )
        return self.locator

    def found_by(self, the_actor: Actor) -> WebElement:
        """
        Get the |WebElement| object representing the targeted element, as
        found by the actor.

        Args:
            the_actor (Actor): The |Actor| who should look for this
                element.

        Returns:
            |WebElement|
        """
        return the_actor.uses_ability_to(BrowseTheWeb).to_find(self)

    def all_found_by(self, the_actor: Actor) -> List[WebElement]:
        """
        Get a list of |WebElement| objects described by the stored locator, as
        found by the actor.

        Args:
            the_actor (Actor): The |Actor| who should look for these
                elements.

        Returns:
            list(|WebElement|)
        """
        return the_actor.uses_ability_to(BrowseTheWeb).to_find_all(self)

    def __init__(self, desc: str) -> None:
        self.target_name = desc
        self.locator = None

    def __repr__(self) -> str:
        return self.target_name
