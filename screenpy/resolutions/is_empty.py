"""
Matches an empty collection.
"""

from hamcrest import empty

from .base_resolution import BaseResolution


class IsEmpty(BaseResolution):
    """Match on an empty collection.

    Examples::

        the_actor.should(See.the(List.of_all(VIDEO_FRAMES), IsEmpty()))
    """

    line = "an empty collection"
    matcher_function = empty
