"""
A resolution that negates another resolution. Resolutions must be paired
with questions and passed together to an actor like so:

    the_actor.should_see_the(
        (Text.of_the(WELCOME_BANNER), IsNot(EqualTo("Goodbye!"))),
    )
"""


from hamcrest import is_not
from hamcrest.core.base_matcher import Matcher

from .base_resolution import BaseResolution


class IsNot(BaseResolution):
    """
    Match a negated Resolution (e.g. `not ReadsExactly("yes")`).
    """

    expected: BaseResolution
    matcher: Matcher[BaseResolution]

    line = "not {expectation}"

    def get_line(self) -> str:
        """Override base get_line because of the unique circumstance."""
        return self.line.format(expectation=self.expected.get_line())

    def __init__(self, resolution: BaseResolution) -> None:
        self.expected = resolution
        self.matcher = is_not(resolution)
