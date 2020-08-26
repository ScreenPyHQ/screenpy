"""
A resolution that matches against a dictionary that contains the specified
key/value pair(s).
"""

from typing import Mapping

from hamcrest import has_entries
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheEntry(BaseResolution):
    """Match a dictionary containing the specified key/value pair(s).

    Examples::

        the_actor.should_see_the(
            (HeadersOfTheLastRequest(), ContainTheEntry(Authorization="Bearer 1"))
        )
    """

    expected: object
    matcher: Matcher[Mapping]

    line = "dict containing {expectation}"

    def __init__(self, **kwargs: object) -> None:
        self.expected = kwargs
        self.matcher = has_entries(**kwargs)
