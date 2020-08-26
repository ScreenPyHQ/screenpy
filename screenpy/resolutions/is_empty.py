"""
A resolution that matches an empty collection.
"""

from typing import Sized

from hamcrest import empty
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class IsEmpty(BaseResolution):
    """Match on an empty collection.

    Examples::

        the_actor.should_see_the((List.of_all(VIDEO_FRAMES), IsEmpty()))
    """

    expected: None
    matcher: Matcher[Sized]

    line = "an empty collection"

    def __init__(self) -> None:
        self.expected = None
        self.matcher = empty()
