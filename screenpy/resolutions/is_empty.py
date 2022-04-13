"""
Matches an empty collection.
"""

from hamcrest import empty
from hamcrest.library.collection.is_empty import IsEmpty as _IsEmpty

from .base_resolution import BaseResolution


class IsEmpty(BaseResolution):
    """Match on an empty collection.

    Examples::

        the_actor.should(See.the(List.of_all(VIDEO_FRAMES), IsEmpty()))
    """

    matcher: _IsEmpty
    line = "an empty collection"
    matcher_function = empty

    def __init__(self) -> None:
        super().__init__()
