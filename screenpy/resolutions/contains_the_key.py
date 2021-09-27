"""
Matches a dictionary that contains the desired key.
"""

from hamcrest import has_key

from .base_resolution import BaseResolution


class ContainsTheKey(BaseResolution):
    """Match a dictionary containing a specific key.

    Examples::

        the_actor.should(See.the(LastResponseBody(), ContainsTheKey("skeleton")))
    """

    line = 'a dict containing the key "{expectation}"'
    matcher_function = has_key
