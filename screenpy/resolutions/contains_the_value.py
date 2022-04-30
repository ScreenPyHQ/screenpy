"""
Matches a dictionary that contains a specific value.
"""

from typing import TypeVar

from hamcrest import has_value
from hamcrest.library.collection.isdict_containingvalue import IsDictContainingValue

from .base_resolution import BaseResolution

V = TypeVar("V")


class ContainsTheValue(BaseResolution):
    """Match a dictionary containing a specific value.

    Examples::

        the_actor.should(
            See.the(Cookies(), ContainTheValue("pumpernickle"))
        )
    """

    matcher: IsDictContainingValue
    line = 'a dict containing the value "{expectation}"'
    matcher_function = has_value

    def __init__(self, value: V) -> None:
        super().__init__(value)
