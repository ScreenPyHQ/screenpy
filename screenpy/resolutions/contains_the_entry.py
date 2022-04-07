"""
Matches a dictionary that contains the specified key/value pair(s).
"""

from hamcrest import has_entries
from hamcrest.library.collection.isdict_containingentries import IsDictContainingEntries

from .base_resolution import BaseResolution


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
