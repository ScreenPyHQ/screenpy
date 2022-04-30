"""
Matches an exact string.
"""

from hamcrest import has_string
from hamcrest.library.object.hasstring import HasString

from .base_resolution import BaseResolution


class ReadsExactly(BaseResolution):
    """Match a specific string exactly.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_MESSAGE), ReadsExactly("Log in below."))
        )
    """

    matcher: HasString
    line = '"{expectation}", verbatim'
    matcher_function = has_string

    def __init__(self, match: str) -> None:
        super().__init__(match)
