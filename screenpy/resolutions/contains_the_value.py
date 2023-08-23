"""
Matches a dictionary that contains a specific value.
"""

from typing import Any, Generic, Mapping, TypeVar

from hamcrest import has_value
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import tostring

V = TypeVar("V")


class ContainsTheValue(Generic[V]):
    """Match a dictionary containing a specific value.

    Examples::

        the_actor.should(
            See.the(Cookies(), ContainTheValue("pumpernickle"))
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Containing the value {tostring(self.value)}."

    @property
    def beatmsg(self) -> str:
        """format string meant for beat msg"""
        return f"... hoping it contains the value {tostring(self.value)}."

    @beat("{beatmsg}")
    def resolve(self) -> Matcher[Mapping[Any, V]]:
        """Produce the Matcher to form the assertion."""
        return has_value(self.value)

    def __init__(self, value: V) -> None:
        self.value = value
