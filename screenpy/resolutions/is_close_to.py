"""
Matches a value that falls within the range specified by the given delta.
"""

from hamcrest import close_to

from .base_resolution import BaseResolution


class IsCloseTo(BaseResolution):
    """Matches a value that falls within the range specified by the given delta.

    Examples::

        the_actor.should(
            See.the(Number.of(BALLOONS), IsCloseTo(FILLED_BALLOONS_COUNT, delta=25))
        )
    """

    matcher_function = close_to

    def get_line(self) -> str:
        """Get the line that describes this Resolution."""
        args, kwargs = self.expected
        return f"a value at most {kwargs['delta']} away from {args[0]}."
