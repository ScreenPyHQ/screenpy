"""
A resolution that matches against a dictionary that contains the specified
key/value pair(s).
"""

from hamcrest import has_entries

from .base_resolution import BaseResolution


class ContainsTheEntry(BaseResolution):
    """Match a dictionary containing the specified key/value pair(s).

    Examples::

        the_actor.should_see_the(
            (HeadersOfTheLastResponse(), ContainTheEntry(Authorization="Bearer 1"))
        )
    """

    line = "dict containing {expectation}"
    matcher_function = has_entries
