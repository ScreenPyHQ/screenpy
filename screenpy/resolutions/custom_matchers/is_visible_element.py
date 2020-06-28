"""
A resolution that matches a visible element. Resolutions must be paired with
questions and passed together to an actor like so:
    the_actor.should_see((TheElement(WELCOME_BANNER), IsVisible()))
"""


from typing import Optional

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from selenium.webdriver.remote.webelement import WebElement


class _IsVisibleElement(BaseMatcher[Optional[object]]):
    """
    Matches an element whose `is_displayed` method returns True.
    """

    def _matches(self, item: Optional[WebElement]) -> bool:
        if item is None:
            return False
        return item.is_displayed()

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text("the element is visible.")

    def describe_mismatch(
        self, item: WebElement, mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        if item is None:
            mismatch_description.append_text("was None")
            return
        mismatch_description.append_text("was not visible.")


def is_visible_element():
    """This matcher matches any element that is visible."""
    return _IsVisibleElement()
