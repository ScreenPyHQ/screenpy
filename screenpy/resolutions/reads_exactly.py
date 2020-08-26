"""
A resolution that matches an exact string.
"""

from hamcrest import has_string
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ReadsExactly(BaseResolution):
    """Match a specific string exactly.

    Examples::

        the_actor.should_see_the(
            (Text.of_the(LOGIN_MESSAGE), ReadsExactly("Log in below."))
        )
    """

    expected: str
    matcher: Matcher[object]

    line = '"{expectation}", verbatim.'

    def __init__(self, string: str) -> None:
        self.expected = string
        self.matcher = has_string(string)
