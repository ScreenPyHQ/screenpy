"""
Make several assertions using any number of Question and Resolution tuples,
all of which are expected to be true.
"""

from typing import Tuple, Type, TypeVar, Union

from screenpy import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.protocols import Answerable
from screenpy.resolutions import BaseResolution

from .see import See

SelfSeeAllOf = TypeVar("SelfSeeAllOf", bound="SeeAllOf")
T_T = Tuple[Union[Answerable, object], BaseResolution]


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
            )
        )
    """

    tests: Tuple[T_T, ...]

    @classmethod
    def the(cls: Type[SelfSeeAllOf], *tests: T_T) -> SelfSeeAllOf:
        """Supply any number of Question/value + Resolution tuples to test."""
        return cls(*tests)

    def describe(self: SelfSeeAllOf) -> str:
        """Describe the Action in present tense."""
        return f"See if all of {self.number_of_tests} tests pass."

    @beat("{} sees if all of the following {number_of_tests} tests pass:")
    def perform_as(self: SelfSeeAllOf, the_actor: Actor) -> None:
        """Direct the Actor to make a series of observations."""
        for question, resolution in self.tests:
            the_actor.should(See.the(question, resolution))

    def __init__(self: SelfSeeAllOf, *tests: T_T) -> None:
        for tup in tests:
            if isinstance(tup, tuple):
                if len(tup) != 2:
                    raise UnableToAct("Tuple must contain Question and Resolution")
            else:
                raise TypeError("Arguments must be tuples")

        self.tests = tests
        self.number_of_tests = len(tests)
