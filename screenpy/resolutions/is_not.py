"""
Matches the negation of another Resolution.
"""

from hamcrest import is_not

from .base_resolution import BaseResolution


class IsNot(BaseResolution):
    """Match a negated Resolution.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsNot(Visible())))
    """

    line = "not {expectation}"
    matcher_function = is_not

    def get_line(self) -> str:
        """Override base get_line to formulate this unique line."""
        return self.line.format(expectation=self.expected.get_line())
