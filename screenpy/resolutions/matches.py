"""
Matches a string using a regex pattern.
"""

from hamcrest import matches_regexp
from hamcrest.library.text.stringmatches import StringMatchesPattern

from .base_resolution import BaseResolution


class Matches(BaseResolution):
    """Match a string using a regular expression.

    Examples::

        the_actor.should(
            # matches "/product/1", "/product/22", "/product/942"...
            See.the(Text.of_the(URL), Matches(r"/product/[0-9]{1,3}"))
        )
    """

    matcher: StringMatchesPattern
    line = 'text matching the regular expression "{expectation}".'
    matcher_function = matches_regexp

    def __init__(self, match: str) -> None:
        super().__init__(match)
