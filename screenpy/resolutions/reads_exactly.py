"""
Matches an exact string.
"""

from hamcrest import has_string

from .base_resolution import BaseResolution


class ReadsExactly(BaseResolution):
    """Match a specific string exactly.

    Examples::

        the_actor.should(
            See.the(Text.of_the(LOGIN_MESSAGE), ReadsExactly("Log in below."))
        )
    """

    line = '"{expectation}", verbatim'
    matcher_function = has_string
