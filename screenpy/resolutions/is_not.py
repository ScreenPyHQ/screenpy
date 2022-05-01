"""
Matches the negation of another Resolution.
"""

from typing import Type, TypeVar, Union

from hamcrest import is_not
from hamcrest.core.core.isnot import IsNot as _IsNot

from .base_resolution import BaseResolution

T = TypeVar("T")


class IsNot(BaseResolution):
    """Match a negated Resolution.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsNot(Visible())))
    """

    matcher: _IsNot
    line = "not {expectation}"
    matcher_function = is_not

    def get_line(self) -> str:
        """Override base get_line to formulate this unique line."""
        return self.line.format(expectation=self.expected.get_line())

    def __init__(self, match: Union[Type, T]) -> None:
        super().__init__(match)
