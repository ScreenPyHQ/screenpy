"""Make an assertion using a Question/value and a Resolution."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hamcrest import assert_that

from screenpy.pacing import aside, beat
from screenpy.protocols import Answerable, ErrorKeeper
from screenpy.speech_tools import get_additive_description, represent_prop

if TYPE_CHECKING:
    from typing import Union

    from typing_extensions import Self

    from screenpy.actor import Actor
    from screenpy.protocols import Resolvable

    T_Q = Union[Answerable, object]
    T_R = Resolvable


class See:
    """See if a value or the answer to a Question matches the Resolution.

    This is a very important Action in ScreenPy; it is the way to perform
    test assertions. For more information, see the documentation for
    :ref:`Questions` and :ref:`Resolutions`.

    Examples::

        the_actor.should(
            See(TheText.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")),
        )

        the_actor.should(
            See.the(list_of_items, ContainsTheItem("juice extractor")),
        )
    """

    question: T_Q
    resolution: T_R

    @classmethod
    def the(cls, question: T_Q, resolution: T_R) -> Self:
        """Supply the Question (or value) and Resolution to test."""
        return cls(question, resolution)

    @property
    def question_to_log(self) -> str:
        """Represent the Question in a log-friendly way."""
        return get_additive_description(self.question)

    @property
    def resolution_to_log(self) -> str:
        """Represent the Resolution in a log-friendly way."""
        return get_additive_description(self.resolution)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"See if {self.question_to_log} is {self.resolution_to_log}."

    @beat("{} sees if {question_to_log} is {resolution_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to make an observation."""
        if isinstance(self.question, Answerable):
            value: object = self.question.answered_by(the_actor)
        else:
            # must be a value instead of a question!
            value = self.question
            aside(f"the actual value is: {represent_prop(value)}")

        reason = ""
        if isinstance(self.question, ErrorKeeper):
            reason = f"{self.question.caught_exception}"

        assert_that(value, self.resolution.resolve(), reason)

    def __init__(self, question: T_Q, resolution: T_R) -> None:
        self.question = question
        self.resolution = resolution
