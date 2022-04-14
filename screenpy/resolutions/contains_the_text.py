"""
Matches a substring.
"""

from hamcrest import contains_string
from hamcrest.library.text.stringcontains import StringContains

from .base_resolution import BaseResolution


class ContainsTheText(BaseResolution):
    """Match a specific substring of a string.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), ContainsTheText("Hello,"))
        )
    """

    matcher: StringContains
    line = 'text containing "{expectation}"'
    matcher_function = contains_string

    def __init__(self, match: str) -> None:
        super().__init__(match)
