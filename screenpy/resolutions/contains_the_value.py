"""
A resolution that matches against a dictionary that contains a specific value.
"""

from typing import Any, Mapping

from hamcrest import has_value
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheValue(BaseResolution):
    """Match a dictionary containing a specific value.

    Examples::

        the_actor.should_see_the(
            (Cookies(), ContainTheValue("pumpernickle"))
        )
    """

    expected: object
    matcher: Matcher[Mapping[Any, object]]

    line = 'dict containing the value "{expectation}"'

    def __init__(self, item: object) -> None:
        self.expected = str(item)
        self.matcher = has_value(item)
