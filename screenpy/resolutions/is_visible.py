"""
A resolution that matches against the visibility of an element. Resolutions
must be paired with questions and passed together to an actor like so:

    the_actor.should_see((TheElement(SUCCESS_MESSAGE), IsVisible()))
"""


from typing import Optional

from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution
from .custom_matchers import is_visible_element


class IsVisible(BaseResolution):
    """
    Match on visibility of an element (i.e. `element.is_displayed()`).
    """

    expected: object
    matcher: Matcher[Optional[object]]

    line = "visible"

    def __init__(self) -> None:
        self.expected = True
        self.matcher = is_visible_element()
