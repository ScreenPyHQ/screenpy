from typing import List, Tuple

from selenium.webdriver.common.by import By

from .abilities.browse_the_web import BrowseTheWeb


class Target(object):
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

    @staticmethod
    def the(desc: str) -> "Target":
        """
        Creates a Target with a description. This method call should be
        followed up with a call to |Target.located_by|.

        Args:
            desc (str): The human-readable description for the targeted
                element. Beginning with a lower-case letter makes the
                allure test logs look the nicest.

        Returns:
            |Target|
        """
        return Target(desc)

    def located_by(self, locator: str) -> "Target":
        """
        Supplies an instantiated Target with a locator string.

        Args:
            locator (str): The string to use as a locator for the element.
                Can be a CSS selector or an xpath string.

        Returns:
            |Target|
        """
        self.locator = locator
        return self

    def get_locator(self) -> Tuple["By", str]:
        """
        Returns the stored locator as a tuple, figuring out what kind of
        location strategy the string uses (CSS selector or xpath).

        Returns:
            tuple(|By|, str)
        """
        if self.locator.startswith("/"):
            return (By.XPATH, self.locator)
        else:
            return (By.CSS_SELECTOR, self.locator)

    def found_by(self, the_actor: "Actor") -> "WebElement":
        """
        Gets the |WebElement| object representing the targeted element.

        Args:
            the_actor (Actor): The |Actor| who should look for this
                element.

        Returns:
            |WebElement|
        """
        return the_actor.uses_ability_to(BrowseTheWeb).find(self.get_locator())

    def all_found_by(self, the_actor: "Actor") -> List["WebElement"]:
        """
        Gets a list of |WebElement| objects described by the stored
        locator.

        Args:
            the_actor (Actor): The |Actor| who should look for these
                elements.

        Returns:
            list(|WebElement|)
        """
        return the_actor.uses_ability_to(BrowseTheWeb).find_all(self.get_locator())

    def __init__(self, desc: str) -> None:
        self.target_name = desc
        self.locator = ""

    def __repr__(self) -> str:
        return self.target_name
