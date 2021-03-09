"""
A resolution that matches against a clickable WebElement.
"""

from typing import Optional

from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution
from .custom_matchers import is_clickable_element


class IsClickable(BaseResolution):
    """Match on a clickable element.

    Examples::

        the_actor.should_see_the((Element(LOGIN_BUTTON), IsClickable()))
    """

    expected: object
    matcher: Matcher[Optional[object]]

    line = "clickable"

    def __init__(self) -> None:
        self.expected = True
        self.matcher = is_clickable_element()
