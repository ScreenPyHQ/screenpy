"""
A resolution that negates another resolution. Resolutions must be paired
with questions and passed together to an actor like so:

    the_actor.should_see_the(
        (Text.of_the(WELCOME_BANNER), IsNot(EqualTo("Goodbye!"))),
    )
"""


from typing import Any

from hamcrest import is_not

from .base_resolution import BaseResolution


class IsNot(BaseResolution):
    """
    Matches a negated Resolution (e.g. `not ReadsExactly("yes")`).
    """

    expected: Any
    matcher: object

    line = "not {expectation}"

    def __init__(self, resolution: Any) -> None:
        self.expected = resolution
        self.matcher = is_not(resolution)
