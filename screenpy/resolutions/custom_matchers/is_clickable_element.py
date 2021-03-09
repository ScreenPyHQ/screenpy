"""
A matcher that matches a clickable element. For example:

    assert_that(driver.find_element_by_id("search"), is_clickable_element())
"""
from typing import Optional

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from selenium.webdriver.remote.webelement import WebElement


class IsClickableElement(BaseMatcher[Optional[object]]):
    """Matches an element which both ``is_enabled`` and ``is_displayed``."""

    def _matches(self, item: Optional[WebElement]) -> bool:
        if item is None:
            return False
        return item.is_displayed() and item.is_enabled()

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text("the element is enabled/clickable.")

    def describe_mismatch(
        self, item: WebElement, mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        if item is None or not item.is_displayed():
            mismatch_description.append_text("was not even present.")
            return
        mismatch_description.append_text("was not enabled/clickable.")


def is_clickable_element() -> IsClickableElement:
    """This matcher matches any element that is enabled."""
    return IsClickableElement()
