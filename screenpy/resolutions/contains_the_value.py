"""Matches a dictionary that contains a specific value."""

from typing import Any, Generic, Mapping, TypeVar

from hamcrest import has_value
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

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
        return f"Containing the value {self.value_to_log}."

    @beat("... hoping it contains the value {value_to_log}.")
    def resolve(self) -> Matcher[Mapping[Any, V]]:
        """Produce the Matcher to form the assertion."""
        return has_value(self.value)

    def __init__(self, value: V) -> None:
        self.value = value
        self.value_to_log = represent_prop(value)
