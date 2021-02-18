"""
Provides an object to store a locator with a human-readable string. The
human-readable string will be used in logging and reporting; the locator
will be used by actors to find elements.
"""

from typing import List, Tuple, Union

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from .abilities.browse_the_web import BrowseTheWeb
from .actor import Actor
from .exceptions import TargetingError


class Target:
    """Describe an element with a human-readable string and a locator.

    Examples::

        Target.the("header search bar").located_by("div.searchbar")

        Target.the("welcome message").located_by('//h2[@name = "welcome"]')
    """

    target_name: str
    locator: Union[None, Tuple[By, str]]

    @staticmethod
    def the(desc: str) -> "Target":
        """Name this target.

        Beginning with a lower-case letter makes the logs look the nicest.
        """
        return Target(desc)

    def located_by(self, locator: Union[Tuple[By, str], str]) -> "Target":
        """Set the locator for this target.

        Possible values for locator:
            * A tuple of a |By| classifier and a string
                (e.g. ``(By.ID, "welcome")``)
            * An XPATH string
                (e.g. ``"//div/h3"``)
            * A CSS selector string
                (e.g. ``"div.confetti"``)
        """
        if isinstance(locator, tuple):
            self.locator = locator
        elif locator.startswith("/"):
            self.locator = (By.XPATH, locator)
        else:
            self.locator = (By.CSS_SELECTOR, locator)

        return self

    located = located_by

    def get_locator(self) -> Tuple[By, str]:
        """Return the stored locator.

        Raises:
            |TargetingError|: if no locator was set.
        """
        if self.locator is None:
            raise TargetingError(
                f"Locator was not supplied to the {self} target. Make sure to use "
                "either .located() or .located_by() to supply a locator."
            )
        return self.locator

    def found_by(self, the_actor: Actor) -> WebElement:
        """Retrieve the |WebElement| as viewed by the actor."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        try:
            return browser.find_element(*self.get_locator())
        except WebDriverException as e:
            raise TargetingError(f"{e} raised while trying to find {self}.") from e

    def all_found_by(self, the_actor: Actor) -> List[WebElement]:
        """Retrieve a list of |WebElement| objects as viewed by the actor."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        try:
            return browser.find_elements(*self.get_locator())
        except WebDriverException as e:
            raise TargetingError(f"{e} raised while trying to find {self}.") from e

    def __repr__(self) -> str:
        return self.target_name

    __str__ = __repr__

    def __init__(self, desc: str) -> None:
        self.target_name = desc
        self.locator = None
