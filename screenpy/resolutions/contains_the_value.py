"""
Matches a dictionary that contains a specific value.
"""

from hamcrest import has_value

from .base_resolution import BaseResolution


class ContainsTheValue(BaseResolution):
    """Match a dictionary containing a specific value.

    Examples::

        the_actor.should(
            See.the(Cookies(), ContainTheValue("pumpernickle"))
        )
    """

    line = 'a dict containing the value "{expectation}"'
    matcher_function = has_value
