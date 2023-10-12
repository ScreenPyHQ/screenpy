"""Matches a dictionary that contains the desired key."""

from typing import Any, Generic, Hashable, Mapping, TypeVar

from hamcrest import has_key
from hamcrest.core.matcher import Matcher

from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

K = TypeVar("K", bound=Hashable)


class ContainsTheKey(Generic[K]):
    """Match a dictionary containing a specific key.

    Examples::

        the_actor.should(See.the(LastResponseBody(), ContainsTheKey("skeleton")))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Containing the key {self.key_to_log}."

    @beat("... hoping it's a dict containing the key {key_to_log}.")
    def resolve(self) -> Matcher[Mapping[K, Any]]:
        """Produce the Matcher to make the assertion."""
        return has_key(self.key)

    def __init__(self, key: K) -> None:
        self.key = key
        self.key_to_log = represent_prop(key)
