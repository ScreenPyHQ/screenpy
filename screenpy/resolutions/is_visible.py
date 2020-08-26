"""
A resolution that matches against the a visible element.
"""

from typing import Optional

from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution
from .custom_matchers import is_visible_element


class IsVisible(BaseResolution):
    """Match on a visible element.

    Examples::

        the_actor.should_see_the((Element(WELCOME_BANNER), IsVisible()))
    """

    expected: object
    matcher: Matcher[Optional[object]]

    line = "visible"

    def __init__(self) -> None:
        self.expected = True
        self.matcher = is_visible_element()
