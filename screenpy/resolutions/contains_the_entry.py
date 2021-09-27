"""
Matches a dictionary that contains the specified key/value pair(s).
"""

from hamcrest import has_entries

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

    line = "a dict containing {expectation}"
    matcher_function = has_entries
