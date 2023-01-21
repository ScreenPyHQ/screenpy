"""
Matches a string which begins with a substring.
"""

from hamcrest import starts_with
from hamcrest.library.text.stringstartswith import StringStartsWith

from .base_resolution import BaseResolution


class StartsWith(BaseResolution):
    """Match a string which starts with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), StartsWith("Welcome"))
        )
    """

    matcher: StringStartsWith
    line = 'text starting with "{expectation}".'
    matcher_function = starts_with

    def __init__(self, match: str) -> None:
        super().__init__(match)
