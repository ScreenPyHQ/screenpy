"""
Matches a substring.
"""

from hamcrest import contains_string

from .base_resolution import BaseResolution


class ContainsTheText(BaseResolution):
    """Match a specific substring of a string.

    Examples::

        the_actor.should(
            See.the(Text.of_the(WELCOME_MESSAGE), ContainsTheText("Hello,"))
        )
    """

    line = 'text containing "{expectation}"'
    matcher_function = contains_string
