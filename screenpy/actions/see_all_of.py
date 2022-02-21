"""
Make several assertions using any number of Question and Resolution tuples,
all of which are expected to be true.
"""

from typing import Tuple

from screenpy import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.protocols import Answerable
from screenpy.resolutions import BaseResolution

from .see import See


class SeeAllOf:
    """See if all the provided values or Questions match their Resolutions.

    Uses :class:`~screenpy.actions.See` to assert all values or the answers to
    the :ref:`Questions` match their paired :ref:`Resolutions`:.

    Examples::

        the_actor.should(
            SeeAllOf(
                (TheText.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")),
                (the_character_speech_bubble, ContainsTheText("Howdy!")),
            )
        )

        the_actor.should(
            SeeAllOf.the(
                (Number.of(BALLOONS), IsEqualTo(3)),
                (Text.of_the(PARADE_FLOAT), ContainsTheText("Congratulations!")),
            )
        )
    """

    @staticmethod
    def the(*tests: Tuple[Answerable, BaseResolution]) -> "SeeAllOf":
        """Supply any number of Question/value + Resolution tuples to test."""
        return SeeAllOf(*tests)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"See if all of {self.number_of_tests} tests pass."

    @beat("{} sees if all of the following {number_of_tests} tests pass:")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to make a series of observations."""
        for question, resolution in self.tests:
            the_actor.should(See.the(question, resolution))

    def __init__(self, *tests: Tuple[Answerable, BaseResolution]) -> None:
        if len(tests) < 2:
            raise UnableToAct(
                "Must supply 2 or more tests for SeeAllOf."
                " Use See instead for single tests."
            )
        self.tests = tests
        self.number_of_tests = len(tests)
