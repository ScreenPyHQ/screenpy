"""
A resolution that matches using equality.
"""

from hamcrest import equal_to

from .base_resolution import BaseResolution


class IsEqualTo(BaseResolution):
    """Match on an equal object.

    Examples::

        the_actor.should_see_the(
            (Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0)),
        )
    """

    line = "equal to {expectation}"
    matcher_function = equal_to
