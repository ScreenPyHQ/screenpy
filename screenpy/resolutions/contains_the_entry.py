"""Matches a dictionary that contains the specified key/value pair(s)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Hashable, Iterable, Mapping, TypeVar, overload

from hamcrest import has_entries

from screenpy.exceptions import UnableToFormResolution
from screenpy.pacing import beat
from screenpy.speech_tools import represent_prop

if TYPE_CHECKING:
    from hamcrest.core.matcher import Matcher

    K = TypeVar("K", bound=Hashable)
    V = TypeVar("V", bound=Any)


class ContainsTheEntry:
    """Match a dictionary containing the specified key/value pair(s).

    Examples::

        the_actor.should(
            See.the(
                HeadersOfTheLastResponse(), ContainTheEntry(Authorization="Bearer 1")
            )
        )

        the_actor.should(
            See.the(
                EnglishDictionary(), ContainsTheEntry({"Python": "a large snake."})
            )
        )

        the_actor.should(See.the(MathTestAnswers(), ContainsTheEntry("Problem3", 45)))
    """

    @property
    def entry_plural(self) -> str:
        """Decide if we need "entry" or "entries" in the beat message."""
        return "entries" if len(self.entries) != 1 else "entry"

    @property
    def entries_to_log(self) -> str:
        """Represent the entries in a log-friendly way."""
        return ", ".join(
            f"{represent_prop(k)}->{represent_prop(v)}" for k, v in self.entries.items()
        )

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"A mapping with the {self.entry_plural} {self.entries_to_log}."

    @beat("... hoping it's a mapping with the {entry_plural} {entries_to_log}")
    def resolve(self) -> Matcher[Mapping]:
        """Produce the Matcher to make the assertion."""
        return has_entries(**self.entries)

    # Keyword argument form
    @overload
    def __init__(self, **kv_args: V) -> None: ...

    # Key to value dict or list of tuples form
    @overload
    def __init__(self, kv_args: Mapping[K, V] | list[tuple[K, V]]) -> None: ...

    # Alternating key/value form
    @overload
    def __init__(self, *kv_args: V) -> None: ...

    def __init__(self, *kv_args: Any, **kv_kwargs: Any) -> None:
        if len(kv_args) > 1 and len(kv_args) % 2 == 1:
            msg = f"{self.__class__.__name__} could not pair {kv_args}."
            msg += " Make sure they're paired up properly!"
            raise UnableToFormResolution(msg)

        if len(kv_args) == 1:
            # given a dictionary or list of tuples
            self.entries = dict(kv_args[0], **kv_kwargs)
        else:
            try:
                # given pairs, keywords, or both
                self.entries = dict(kv_args, **kv_kwargs)
            except ValueError:
                # given a list of implicitly paired arguments
                pairs: Iterable[tuple[Any, Any]] = [
                    (kv_args[i], kv_args[i + 1]) for i in range(0, len(kv_args), 2)
                ]
                self.entries = dict(pairs, **kv_kwargs)
