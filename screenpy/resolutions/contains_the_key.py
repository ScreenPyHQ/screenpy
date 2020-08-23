"""
A resolution that matches against a dictionary that contains the desired key.
Resolutions must be paired with questions and passed together to an actor:

    the_actor.should_see_the(
        (LastResponseBody(), ContainsTheKey("token")),
    )
"""

from typing import Any, Hashable, Mapping

from hamcrest import has_key
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class ContainsTheKey(BaseResolution):
    """
    Match a dictionary containing a key (e.g. `"play" in {"play": "Hamlet"}`).
    """

    expected: object
    matcher: Matcher[Mapping[Hashable, Any]]

    line = 'dict containing the key "{expectation}"'

    def __init__(self, key: Hashable) -> None:
        self.expected = str(key)
        self.matcher = has_key(key)
