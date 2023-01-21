"""
Matches a string which ends with a substring.
"""

from hamcrest import ends_with
from hamcrest.library.text.stringendswith import StringEndsWith

from .base_resolution import BaseResolution


class EndsWith(BaseResolution):
    """Match a string which ends with the given substring.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_ERROR), EndsWith("username or password."))
        )
    """

    matcher: StringEndsWith
    line = 'text ending with "{expectation}".'
    matcher_function = ends_with

    def __init__(self, match: str) -> None:
        super().__init__(match)
