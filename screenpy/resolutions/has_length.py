"""
Matches the length of a collection.
"""

from hamcrest import has_length
from hamcrest.library.object.haslength import HasLength as _HasLength

from .base_resolution import BaseResolution


class HasLength(BaseResolution):
    """Match against a collection with a specific length.

    Examples::

        the_actor.should(
            See.the(Selected.options_from(INDUSTRIES), HasLength(5))
        )
    """

    matcher: _HasLength
    line = "a collection with {expectation} items in it"
    matcher_function = has_length

    def __init__(self, match: int) -> None:
        super().__init__(match)
