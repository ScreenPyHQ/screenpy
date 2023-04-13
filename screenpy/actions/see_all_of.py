"""
Make several assertions using any number of Question and Resolution tuples,
all of which are expected to be true.
"""

from typing import Tuple, Type, TypeVar

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat

from .see import T_Q, T_R, See

SelfSeeAllOf = TypeVar("SelfSeeAllOf", bound="SeeAllOf")
T_T = Tuple[T_Q, T_R]


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
        return f"See if {self.log_message}."

    @beat("{} sees if {log_message}:")
    def perform_as(self: SelfSeeAllOf, the_actor: Actor) -> None:
        """Direct the Actor to make a series of observations."""
        all_passed = True
        for question, resolution in self.tests:
            try:
                the_actor.should(See.the(question, resolution))
            except AssertionError:
                all_passed = False

        if not all_passed:
            raise AssertionError(f"{the_actor} did not find all expected answers!")

    def __init__(self: SelfSeeAllOf, *tests: T_T) -> None:
        if not tests:
            raise UnableToAct("SeeAllOf was not given any tests.")
        for tup in tests:
            if isinstance(tup, tuple):
                if len(tup) != 2:
                    raise UnableToAct("Tuple must contain Question and Resolution.")
            else:
                raise TypeError("Arguments must be tuples.")

        self.tests = tests
        if len(self.tests) == 1:
            self.log_message = "1 test passes"
        else:
            self.log_message = f"all of {len(self.tests)} tests pass"
