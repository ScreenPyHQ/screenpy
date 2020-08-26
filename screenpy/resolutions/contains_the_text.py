"""
A resolution that matches against a substring.
"""

from hamcrest import contains_string
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheText(BaseResolution):
    """Match a specific substring of a string.

    Examples::

        the_actor.should_see_the(
            (Text.of_the(WELCOME_MESSAGE), ContainsTheText("Hello,"))
        )
    """

    expected: str
    matcher: Matcher[str]

    line = 'text containing "{expectation}"'

    def __init__(self, substring: str) -> None:
        self.expected = substring
        self.matcher = contains_string(substring)
