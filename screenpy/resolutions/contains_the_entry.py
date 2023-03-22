"""
Matches a dictionary that contains the specified key/value pair(s).
"""

from typing import Any, Hashable, Iterable, Mapping, Tuple, TypeVar, overload

from hamcrest import has_entries
from hamcrest.core.matcher import Matcher

from screenpy.exceptions import UnableToFormResolution
from screenpy.pacing import beat

from .base_resolution import BaseResolution

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class ContainsTheEntry(BaseResolution):
    """Match a dictionary containing the specified key/value pair(s).

    Examples::

        the_actor.should(
            See.the(
                HeadersOfTheLastResponse(), ContainTheEntry(Authorization="Bearer 1")
            )
        )
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"A mapping with the entries {self.entries_to_log}."

    @beat("... hoping it's a mapping with the entries {entries_to_log}")
    def resolve(self) -> Matcher[Mapping]:
        """Produce the Matcher to make the assertion."""
        return has_entries(**self.entries)

    # Keyword argument form
    @overload
    def __init__(self, **kv_args: V) -> None:
        ...

    # Key to value dict form
    @overload
    def __init__(self, kv_args: Mapping[K, V]) -> None:
        ...

    # Alternating key/value form
    @overload
    def __init__(self, *kv_args: Any) -> None:
        ...

    def __init__(self, *kv_args: Any, **kv_kwargs: Any) -> None:
        if len(kv_args) > 1 and len(kv_args) % 2 == 1:
            msg = f"{self.__class__.__name__} could not pair {kv_args}."
            msg += " Make sure they're paired up properly!"
            raise UnableToFormResolution(msg)

        if len(kv_args) == 1:
            # given a dictionary
            self.entries = dict(kv_args[0], **kv_kwargs)
        else:
            try:
                # given pairs, keywords, or both
                self.entries = dict(kv_args, **kv_kwargs)
            except ValueError:
                # given a list of implicitly paired arguments
                pairs: Iterable[Tuple[Any, Any]] = [
                    (kv_args[i], kv_args[i + 1]) for i in range(0, len(kv_args), 2)
                ]
                self.entries = dict(pairs, **kv_kwargs)
        self.entries_to_log = ", ".join(
            f"{{{k}: {v}}}" for k, v in self.entries.items()
        )
