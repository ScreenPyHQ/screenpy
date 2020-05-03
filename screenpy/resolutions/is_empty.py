"""
A resolution that matches an empty collection. Resolutions must be paired
with questions and passed together to an actor like so:

    the_actor.should_see_the((List.of_the(TODO_ITEMS), IsEmpty()))
"""


from hamcrest import empty
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class IsEmpty(BaseResolution):
    """
    Match on an empty collection (e.g. `[]`).
    """

    expected: None
    matcher: Matcher

    line = "an empty collection"

    def __init__(self) -> None:
        self.expected = None
        self.matcher = empty()
