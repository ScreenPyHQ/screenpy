"""Matches a dictionary that contains a specific value."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar

from hamcrest import has_value

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

if TYPE_CHECKING:
    from hamcrest.core.matcher import Matcher

V = TypeVar("V")


class ContainsTheValue(Generic[V]):
    """Match a dictionary containing a specific value.

    Examples::

        the_actor.should(
            See.the(Cookies(), ContainTheValue("pumpernickle"))
        )
    """

    @property
    def value_to_log(self) -> str | V:
        """Represent the value in a log-friendly way."""
        return represent_prop(self.value)

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Containing the value {self.value_to_log}."

    @beat("... hoping it contains the value {value_to_log}.")
    def resolve(self) -> Matcher[Mapping[Any, V]]:
        """Produce the Matcher to form the assertion."""
        return has_value(self.value)

    def __init__(self, value: V) -> None:
        self.value = value
