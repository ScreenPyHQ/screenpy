"""
Make several assertions using any number of Question and Resolution tuples,
at least one of which is expected to be true.
"""

from typing import Tuple

from screenpy import Actor
from screenpy.pacing import beat
from screenpy.protocols import Answerable
from screenpy.resolutions import BaseResolution

from .see import See


class SeeAnyOf:
    """See if at least one |Question| gives its expected answer.

    Examples::

        the_actor.should(
            SeeAnyOf(
                (TheText.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")),
                (TheText.of_the(SPEECH_BUBBLE), ContainsTheText("Howdy!")),
            ),
            SeeAnyOf.the(
                (Number.of(BALLOONS), IsEqualTo(3)),
                (Number.of(BALLOONS), IsEqualTo(4)),
                (Number.of(BALLOONS), IsEqualTo(5)),
            ),
        )
    """

    @staticmethod
    def the(*tests: Tuple[Answerable, BaseResolution]) -> "SeeAnyOf":
        """Supply the |Question| and |Resolution| tuples to assert."""
        return SeeAnyOf(*tests)

    @beat("{} looks for at least 1 expected answer out of {number_of_tests}...")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to make a series of observations."""
        none_passed = True
        for question, resolution in self.tests:
            try:
                the_actor.should(See.the(question, resolution))
                none_passed = False
            except AssertionError:
                pass

        if none_passed:
            raise AssertionError(f"{the_actor} did not find any expected answers!")

    def __init__(self, *tests: Tuple[Answerable, BaseResolution]) -> None:
        self.tests = tests
        self.number_of_tests = len(tests)
