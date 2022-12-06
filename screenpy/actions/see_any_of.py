"""
Make several assertions using any number of Question and Resolution tuples,
at least one of which is expected to be true.
"""

from typing import Tuple, Type, TypeVar, Union

from screenpy import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.protocols import Answerable
from screenpy.resolutions import BaseResolution

from .see import See

SelfSeeAnyOf = TypeVar("SelfSeeAnyOf", bound="SeeAnyOf")
T_T = Tuple[Union[Answerable, object], BaseResolution]


class SeeAnyOf:
    """See if at least one value or Question matches its Resolution.

    Uses :class:`~screenpy.actions.See` to assert at least one of the
    values or the answers to the :ref:`Questions` match their paired
    :ref:`Resolutions`:.

    Examples::

        the_actor.should(
            SeeAnyOf(
                (TheText.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")),
                (the_character_speech_bubble, ContainsTheText("Howdy!")),
            )
        )

        the_actor.should(
            SeeAnyOf.the(
                (Number.of(BALLOONS), IsEqualTo(4)),
            )
        )
    """

    tests: Tuple[T_T, ...]

    @classmethod
    def the(cls: Type[SelfSeeAnyOf], *tests: T_T) -> SelfSeeAnyOf:
        """Supply any number of Question/value + Resolution tuples to test."""
        return cls(*tests)

    def describe(self: SelfSeeAnyOf) -> str:
        """Describe the Action in present tense."""
        return f"See if any of {self.number_of_tests} tests pass."

    @beat("{} sees if any of the following {number_of_tests} tests pass:")
    def perform_as(self: SelfSeeAnyOf, the_actor: Actor) -> None:
        """Direct the Actor to make a series of observations."""
        none_passed = True
        for question, resolution in self.tests:
            try:
                the_actor.should(See.the(question, resolution))
                none_passed = False
            except AssertionError:
                pass  # well, not *pass*, but... you get it.

        if none_passed:
            raise AssertionError(f"{the_actor} did not find any expected answers!")

    def __init__(self: SelfSeeAnyOf, *tests: T_T) -> None:
        for tup in tests:
            if isinstance(tup, tuple):
                if len(tup) != 2:
                    raise UnableToAct("Tuple must contain Question and Resolution")
            else:
                raise TypeError("Arguments must be tuples")

        self.tests = tests
        self.number_of_tests = len(tests)
