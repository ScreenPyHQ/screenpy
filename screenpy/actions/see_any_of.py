"""
Make several assertions using any number of Question and Resolution tuples,
at least one of which is expected to be true.
"""

from typing import Tuple, Type, TypeVar

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat

from .see import T_Q, T_R, See

SelfSeeAnyOf = TypeVar("SelfSeeAnyOf", bound="SeeAnyOf")
T_T = Tuple[T_Q, T_R]


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
        return f"See if {self.log_message}."

    @beat("{} sees if {log_message}:")
    def perform_as(self: SelfSeeAnyOf, the_actor: Actor) -> None:
        """Direct the Actor to make a series of observations."""
        if not self.tests:
            # No tests is OK!
            return

        for question, resolution in self.tests:
            try:
                the_actor.should(See.the(question, resolution))
                break
            except AssertionError:
                pass  # well, not *pass*, but... you get it.
        else:
            # none passed!
            msg = f"{the_actor} did not find any expected answers!"
            raise AssertionError(msg)

    def __init__(self: SelfSeeAnyOf, *tests: T_T) -> None:
        for tup in tests:
            if isinstance(tup, tuple):
                if len(tup) != 2:
                    raise UnableToAct("Tuple must contain Question and Resolution")
            else:
                raise TypeError("Arguments must be tuples")

        self.tests = tests
        if len(self.tests) == 0:
            self.log_message = "no tests pass 🤔"
        elif len(self.tests) == 1:
            self.log_message = "1 test passes"
        else:
            self.log_message = f"any of {len(self.tests)} tests pass"
