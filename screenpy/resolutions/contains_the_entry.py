"""
Matches a dictionary that contains the specified key/value pair(s).
"""

from typing import Any, Hashable, Mapping, TypeVar, overload

from hamcrest import has_entries
from hamcrest.library.collection.isdict_containingentries import IsDictContainingEntries

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

    matcher: IsDictContainingEntries
    line = "a dict containing {expectation}"
    matcher_function = has_entries

    # Keyword argument form
    @overload
    def __init__(self, **keys_valuematchers: V) -> None:
        ...

    # Key to matcher dict form
    @overload
    def __init__(self, keys_valuematchers: Mapping[K, V]) -> None:
        ...

    # Alternating key/matcher form
    @overload
    def __init__(self, *keys_valuematchers: Any) -> None:
        ...

    def __init__(self, *keys_valuematchers: Any, **kv_args: Any) -> None:
        super().__init__(*keys_valuematchers, **kv_args)
