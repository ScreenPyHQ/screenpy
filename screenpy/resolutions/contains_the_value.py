"""
A resolution that matches against a dictionary that contains the desired value.
Resolutions must be paired with questions and passed together to an actor:

    the_actor.should_see_the(
        (LastResponseBody(), ContainsTheValue("gold")),
    )
"""

from typing import Any, Mapping

from hamcrest import has_value
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheValue(BaseResolution):
    """
    Match a dictionary containing a value
    (e.g. `"Hamlet" in {"play": "Hamlet"}.values()`).
    """

    expected: object
    matcher: Matcher[Mapping[Any, object]]

    line = 'dict containing the value "{expectation}"'

    def __init__(self, item: object) -> None:
        self.expected = str(item)
        self.matcher = has_value(item)
