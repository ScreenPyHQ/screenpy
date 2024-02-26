"""Matches the negation of another Resolution."""

from typing import TypeVar

from hamcrest import is_not
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.protocols import Resolvable
from screenpy.speech_tools import get_additive_description

T = TypeVar("T")


class IsNot:
    """Match a negated Resolution.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsNot(Visible())))
    """

    @property
    def resolution_to_log(self) -> str:
        """Represent the Resolution in a log-friendly way."""
        return get_additive_description(self.resolution)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Not {self.resolution_to_log}."

    @beat("... hoping it's not {resolution_to_log}.")
    def resolve(self) -> Matcher[object]:
        """Produce the Matcher to make the assertion."""
        return is_not(self.resolution.resolve())

    def __init__(self, resolution: Resolvable) -> None:
        self.resolution = resolution
