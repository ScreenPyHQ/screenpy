"""
A resolution that matches against a dictionary that contains the specified
key/value pair(s). Resolutions must be paired with questions and passed
together to an actor:

    the_actor.should_see_the(
        (LastResponseBody(), ContainsTheEntry(token="foo")),
    )

    the_actor.should_see_the(
        (LastResponseBody(), ContainsTheEntries(token="foo", value="gold")),
    )
"""

from typing import Mapping

from hamcrest import has_entries
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheEntry(BaseResolution):
    """
    Match a dictionary containing the specified key/value pair(s)
    (e.g. `("play", "Hamlet") in {"play": "Hamlet"}.items()`).
    """

    expected: object
    matcher: Matcher[Mapping]

    line = "dict containing {expectation}"

    def __init__(self, **kwargs: object) -> None:
        self.expected = kwargs
        self.matcher = has_entries(**kwargs)
