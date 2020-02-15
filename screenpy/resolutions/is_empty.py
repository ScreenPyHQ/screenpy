"""
A resolution that matches an empty collection. Resolutions must be paired
with questions and passed together to an actor like so:

    the_actor.should_see_the((List.of_the(TODO_ITEMS), IsEmpty()))
"""


from hamcrest import empty

from .base_resolution import BaseResolution


class IsEmpty(BaseResolution):
    """
    Matches on an empty collection (e.g. `[]`).
    """

    expected: None
    matcher: object

    line = "an empty collection"

    def __init__(self) -> None:
        self.expected = None
        self.matcher = empty()
